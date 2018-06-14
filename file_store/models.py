"""FileStore models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from meta_info.models import MetaInfo


TAGS = (
    'Hero',
)


class FileMixin(models.Model):
    """Mixin for a basic file model."""

    title = models.CharField(
        max_length=200,
        db_index=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
    )
    extension = models.CharField(
        max_length=20,
        blank=True,
    )
    mime = models.CharField(
        max_length=50,
        blank=True,
    )
    source_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Image(FileMixin, ProfileReferredMixin, PreserveModelMixin):
    """Image model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_FILESTORE_IMAGE,
    )
    image = models.ImageField()
    original = models.ForeignKey(
        'file_store.DisplayImage',
        related_name='sizes',
        verbose_name=_('Cropped Images'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='files+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Imagable(models.Model):
    """Mixin to enable the storage of images against an object."""

    images = models.ManyToManyField(
        Image,
        related_name='object+',
        verbose_name=_('Images'),
        blank=True,
    )

    class Meta:
        abstract = True


class Document(FileMixin, ProfileReferredMixin, PreserveModelMixin):
    """Publication file model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_FILESTORE_DOCUMENT,
    )
    file = models.FileField(
        null=True,
    )
    book = models.ForeignKey(
        'books.Book',
        related_name='files',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='files+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
