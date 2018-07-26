"""Tag signals."""

from django.db.models.signals import (pre_save, post_save, )
from django.dispatch import receiver

from meta_info.models import MetaInfo
from file_store.models import Image, Document


@receiver(pre_save, sender=Image)
def pre_save_add_meta_info_image(sender, instance, *args, **kwargs):
    """set meta info for instance."""
    if not instance.pk and not instance.meta_info:
        json = {
            'primaries': [],
        }
        instance.meta_info = MetaInfo.objects.create(
            json=json,
        )


@receiver(post_save, sender=Image)
def post_save_image(sender, instance, *args, **kwargs):
    """Manage the saving of an Image or document with a source_url field.

    Handle the creation of Image and Documents through a secondary model
    to define the state of the download while allowing a service to manage
    the actual retrieval of the file.

    Dedicated service for download is preferred due to external file checks,
    viruses, encoding, broken or slow transfers, are all completed external
    from API interaction.

    Not implemented yet.
    """
    pass


@receiver(pre_save, sender=Document)
def pre_save_add_meta_info_document(sender, instance, *args, **kwargs):
    """set meta info for instance."""
    if not instance.pk and not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()
