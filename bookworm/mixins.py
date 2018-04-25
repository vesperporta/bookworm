"""General mixins."""

import json
import logging
import importlib

from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from model_utils.managers import QueryManager

from bookworm.managers import PreserveModelManager
from bookworm.exceptions import (
    PublishableObjectNotDefined,
    PublishableValidationError,
)


logger = logging.getLogger(__name__)


class CreatedModelMixin(models.Model):
    """Modified field mixin."""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class ModifiedModelMixin(CreatedModelMixin):
    """Modified field mixin."""

    modified_at = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


class PreserveModelMixin(ModifiedModelMixin):
    """Base model to handle core objects.

    Defines created, modified, and deleted fields.
    Prevents deletion of this model and flags for exclusion from results.
    """

    deleted_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        default=None,
    )

    # objects = PreserveModelManager()
    objects = QueryManager(deleted_at__isnull=True)
    all_objects = models.Manager()
    deleted_objects = QueryManager(deleted_at__isnull=False)

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        bool(self.deleted_at)

    def delete(self, *args, **kwargs):
        pre_delete.send(sender=self.__class__, instance=self)
        self.deleted_at = now()
        self.__class__.objects.filter(pk=self.pk).update(
            deleted_at=self.deleted_at
        )
        post_delete.send(sender=self.__class__, instance=self)


class ProfileReferredMixin(models.Model):
    """Profile association mixin."""

    profile = models.ForeignKey(
        'authentication.Profile',
        related_name='+',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True


class PublishableModelMixin(models.Model):
    """Enable a model to be publishable and visible to public view."""

    PUBLISHED_SOURCE_KEY = 'source'

    published_content = models.ForeignKey(
        'meta_info.MetaInfo',
        related_name='published_content+',
        verbose_name=_('Published Content'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def published(self):
        return bool(self.published_at)

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

    def _get_MetaInfo(self):
        module = importlib.import_module('meta_info.models')
        return getattr(module, 'MetaInfo')

    def publish(self):
        """Publish this object"""
        self._validate_for_publication(publish=True)
        self._handle_child_publication(publish=True)
        output_source = {
            self.PUBLISHED_SOURCE_KEY: {
                'id': self.id,
                'class': self.__class__,
            },
        }
        output = self.Publishable.serializer(self).data
        output.update(output_source)
        meta_info_class = self._get_MetaInfo()
        meta_info = meta_info_class(
            json=output,
            copy=json.dumps(output),
        )
        meta_info.save()
        self.published_content = meta_info
        self.published_at = self.published_content.created_at
        self.save()

    def unpublish(self):
        """Unpublish this object"""
        self._validate_for_publication(publish=False)
        self._handle_child_publication(publish=False)
        self.published_at = None
        self.published_content = None
        self.save()

    def unpublish_purge(self):
        """Unpublishes content and removes all history.

        Retainment of datetime stamps of previous publishes with no content.
        """
        self.unpublish()
        meta_info_class = self._get_MetaInfo()
        published_meta_list = meta_info_class.objects.filter(
            json__source__id=self.id,
            json__source__class=self.__class__,
        )
        for item in list(published_meta_list):
            for key in item.json.keys():
                if key is not self.PUBLISHED_SOURCE_KEY:
                    item.json.pop(key)
            item.copy = json.dumps(item.json)
            item.save()
