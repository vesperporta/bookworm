"""Tag signals."""

import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import (Emote, Emotable, Post, Comment)
from meta_info.models import MetaInfo


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Post)
@receiver(pre_save, sender=Comment)
def pre_save_create_meta_info(sender, instance, *args, **kwargs):
    """Pre save ad meta info object."""
    if not instance.pk and not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()


@receiver(pre_save, sender=Emotable)
def pre_save_create_emotable(sender, instance, *args, **kwargs):
    """Pre save ad meta info object."""
    if instance.emote_aggregate:
        return
    instance.emote_aggregate = [0 for k in enumerate(Emote.EMOTES)]
