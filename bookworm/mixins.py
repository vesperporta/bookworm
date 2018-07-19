"""General mixins."""

import logging

from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.utils.timezone import now

from model_utils.managers import QueryManager


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

    objects = QueryManager(deleted_at__isnull=True)
    all_objects = models.Manager()
    deleted_objects = QueryManager(deleted_at__isnull=False)

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return bool(self.deleted_at)

    def delete(self, *args, **kwargs):
        pre_delete.send(sender=self.__class__, instance=self)
        self.deleted_at = now()
        self.__class__.objects.filter(id=self.id).update(
            deleted_at=self.deleted_at,
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
