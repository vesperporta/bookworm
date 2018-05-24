"""Tag signals."""

import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import (Emote, Post)
from meta_info.models import MetaInfo


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Post)
def pre_save_create_meta_info(sender, instance, *args, **kwargs):
    """Pre save ad meta info object."""
    if not instance.emote_aggregate:
        instance.emote_aggregate = [0 for k in enumerate(Emote.EMOTES)]
    if instance.pk:
        return
    if not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()
