"""FileStore models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from file_store.tasks import image_auto_crop_task
from meta_info.models import MetaInfo


TAGS = ()


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
    mime = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    source_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Image(FileMixin, ProfileReferredMixin, PreserveModelMixin):
    """Image model.

    Inherently part of an album through the Imagable mixin.
    """

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_FILESTORE_IMAGE,
    )
    image = models.ImageField()
    original = models.ForeignKey(
        'file_store.Image',
        related_name='sizes',
        verbose_name=_('Cropped Images'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='images+',
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
        related_name='albums+',
        verbose_name=_('Images'),
        blank=True,
    )
    cover_image = models.ForeignKey(
        Image,
        related_name='album_covers+',
        verbose_name=_('Cover Image'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def image_append(self, image, as_primary=False):
        """Append an image to the images list.

        @:param image: Image object.
        @:param as_primary: bool, default = False, assign as cover_image.
        """
        if image.original:
            image = image.original
        if not as_primary and self.images.count() < 1:
            as_primary = True
        if as_primary:
            self.cover_image = image
        if not image.original and image.sizes.count() == 0:
            image_auto_crop_task.delay(image)
        self.images.add(image)

    def image_pop(self, image):
        """Remove an image from the images list.

        If the image being removed is cover_image then the first image not
        the removed image is used as cover_image or None.

        @param image: Image object.
        """
        if image.original:
            size_ids = [image.original.id]
            size_ids += image.original.sizes.values_list('id')
            removals = self.images.filter(id__in=size_ids)
            for remove in removals:
                self.images.remove(remove)
        else:
            self.images.remove(image)
        if self.cover_image == image and self.images.count() > 1:
            self.cover_image = self.images.first()
            self.save()


class Document(FileMixin, ProfileReferredMixin, PreserveModelMixin):
    """Publication file model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_FILESTORE_DOCUMENT,
    )
    file = models.FileField(
        null=True,
    )
    cover = models.ForeignKey(
        Image,
        related_name='covers+',
        verbose_name=_('Cover Image'),
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


class DocumentRefferedMixin(models.Model):
    """Mixin referring to a document."""

    document = models.ForeignKey(
        Document,
        related_name='coffee_table+',
        verbose_name=_('Document'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Documentable(models.Model):
    """Mixin supplying documentation / files."""

    documents = models.ManyToManyField(
        Document,
        related_name='shelves',
        verbose_name=_('Documents'),
        blank=True,
    )

    class Meta:
        abstract = True
