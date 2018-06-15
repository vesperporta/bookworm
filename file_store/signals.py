"""Tag signals."""

from django.db.models.signals import pre_save
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


@receiver(pre_save, sender=Document)
def pre_save_add_meta_info_document(sender, instance, *args, **kwargs):
    """set meta info for instance."""
    if not instance.pk and not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()
