"""General mixins."""

import json
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from meta_info.models import MetaInfo
from bookworm.exceptions import (
    PublishableObjectNotDefined,
    PublishableValidationError,
)


logger = logging.getLogger(__name__)


class PublishableModelMixin(models.Model):
    """Enable a model to be publishable and visible to public view."""

    PUBLISHED_SOURCE_KEY = 'source'

    published_content = models.ForeignKey(
        MetaInfo,
        related_name='published_content+',
        verbose_name=_('Published Content'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(
        verbose_name=_('Published date'),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def published(self):
        """Published state of this model."""
        return bool(self.published_at)

    @property
    def published_json(self):
        """Content expected to publically rendered."""
        if not self.published:
            return None
        content = self.published_content
        content.pop(self.PUBLISHED_SOURCE_KEY)
        return content

    def _validate_for_publication(self, publish=True):
        """Passes `publishable_verification` for fields required verified.

        This value should be a list of lists or tuples of the following format:
        (
        [0]    'field name',
        [1]    ['field value', 'other value', ],
        [2]    'error message optional',
        )

        Additional values can be passed to allow error message rendering
        with better details, an example: 'error from {3} with value {4}'.
        """
        valid = True
        errors = {}
        if not hasattr(self, 'Publishable'):
            publish_type = 'publish' if publish else 'unpublish'
            raise PublishableObjectNotDefined(self, publish_type)
        if not self.Publishable.publishable_verification or not publish:
            return valid
        for obj in self.Publishable.publishable_verification:
            field = getattr(self, obj[0], None)
            msg = 'Field {0} is not equal or not in {1}'
            if field != obj[1] or field not in obj[1]:
                valid = False
                if obj[2]:
                    msg = obj[2]
                errors[obj[0]] = [msg.format(*obj)]
        if errors:
            raise PublishableValidationError(errors)
        return valid

    def _handle_child_publication(self, publish=True):
        """Publish chain for child objects known"""
        if not self.Publishable.publishable_children:
            return
        for obj in self.Publishable.publishable_children:
            child = getattr(self, obj, None)
            if not child:
                continue
            try:
                if publish:
                    child.publish()
                else:
                    child.unpublish()
            except AttributeError:
                logger.warn(
                    'Publish attempt on unpublishable child object {}.'.format(
                        child
                    )
                )

    def publish(self, skip_children=False):
        """Publish this object.

        @param skip_children=False flag to handle child object publication.
        """
        self._validate_for_publication(publish=True)
        if not skip_children:
            self._handle_child_publication(publish=True)
        output_source = {
            self.PUBLISHED_SOURCE_KEY: {
                'id': self.id,
                'class': self.__class__,
            },
        }
        output = self.Publishable.serializer(self).data
        output.update(output_source)
        meta_info = MetaInfo.objects.create(
            json=output,
            copy=json.dumps(output),
        )
        if self.published_content:
            self.published_content.delete()
        self.published_content = meta_info
        self.published_at = self.published_content.created_at
        self.save()

    def unpublish(self, skip_children=False):
        """Unpublish this object.

        @param skip_children=False flag to handle child object publication.
        """
        self._validate_for_publication(publish=False)
        if not skip_children:
            self._handle_child_publication(publish=False)
        self.published_at = None
        self.published_content.delete()
        self.published_content = None
        self.save()

    def unpublish_purge(self):
        """Unpublishes content and removes all history.

        Retainment of datetime stamps of previous publishes with no content.
        """
        self.unpublish()
        published_meta_list = MetaInfo.objects.filter(
            json__source__id=self.id,
            json__source__class=self.__class__,
        )
        for item in list(published_meta_list):
            for key in item.json.keys():
                if key is not self.PUBLISHED_SOURCE_KEY:
                    item.json.pop(key)
            item.copy = json.dumps(item.json)
            item.save()
