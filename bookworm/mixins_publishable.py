"""General mixins."""

import json
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from meta_info.models import HashedTag, MetaInfo
from bookworm.exceptions import (
    PublishableObjectNotDefined,
    PublishableValidationError,
    NoPublishedDataError,
)


logger = logging.getLogger(__name__)


TAGS = (
    'Global',
    'No-one',
)


class PublishableModelMixin(models.Model):
    """Enable a model to be publishable and visible to public view."""

    published_meta = models.ForeignKey(
        MetaInfo,
        related_name='published_meta+',
        verbose_name=_('Published Content'),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def published_at(self):
        return self.published_meta.created_at if self.published_meta else None

    @property
    def published_content(self):
        try:
            return self.published_meta.json.output
        except AttributeError:
            raise NoPublishedDataError(self)

    def has_published_naive_access(self, object_id):
        """Identify if the `object_id` can access this object.

        Will return `False, None` if self has no published data.

        @:param id, str of identifier requesting access.

        @:return bool, int
        Integer is the index within the tuple access is granted.
        """
        if not self.published_at:
            return False, None
        published_access = self.published_meta.json.access
        try:
            id_index = published_access.granted_flat.index(object_id)
            return True, id_index
        except ValueError:
            return False, None

    def _validate_publish(self, granted_list, block_list):
        """Validate the publishable state of this object with parameters.

        @:param granted_list, tuple supplied to `self.publish`.
        @:param block_list, tuple supplied to `self.publish`.

        @:see self.publish

        @:raises PublishableObjectNotDefined
        @:raises PublishableValidationError
        """
        publishable_class = getattr(self, 'Publishable', None)
        if not publishable_class:
            raise PublishableObjectNotDefined(self)
        validate_errors = ()
        if not hasattr(publishable_class, 'serializer'):
            validate_errors += ('Publishable class has no serializer.', )
        if len(granted_list) < 1:
            validate_errors += ('Publishing with no granted objects.', )
        granted_numerical = sum([len(n) for n in granted_list]) % 2
        block_numerical = sum([len(n) for n in block_list]) % 2
        if granted_numerical + block_numerical > 0:
            validate_errors += ('Format of grant and block lists invalid', )
        if validate_errors:
            raise PublishableValidationError(self, validate_errors)

    def publish(self, granted_list, block_list):
        """Publish this object.

        management of what is access and blocked:
        (
            ('global', 'keyword'),
            ('id', '__class__'),
        )

        @:param granted_list, tuple as described above.
        @:param block_list, tuple as described above.

        @:raises PublishableObjectNotDefined
        """
        self._validate_publish(granted_list, block_list)
        output_source = {
            'source': {
                'id': self.id,
                'class': self.__class__,
            },
            'access': {
                'granted': granted_list,
                'granted_flat': [n[0] for n in granted_list],
                'denied': block_list,
                'denied_flat': [n[0] for n in block_list],
            },
            'output': getattr(self, 'Publishable').serializer(self).data,
        }
        if self.published_meta:
            self.published_meta.delete()
        self.published_meta = MetaInfo.objects.create(
            json=output_source,
            copy=json.dumps(output_source),
        )
        self.save()

    def unpublish(self):
        """Un-publish this object."""
        if not self.published_meta:
            raise PublishableValidationError(
                self,
                ('No published data to un-publish', ),
            )
        self.published_meta.delete()
        self.published_meta = None
        self.save()

    def unpublish_purge(self):
        """Un-publishes content and removes all output history."""
        self.unpublish()
        published_meta_list = MetaInfo.all_objects.filter(
            json__source__id=self.id,
            json__source__class=self.__class__,
        )
        for item in list(published_meta_list):
            if not hasattr(item.json, 'output'):
                continue
            item.json.pop('output')
            item.copy = json.dumps(item.json)
            item.save()
