"""Profile signals."""

import logging

from django.conf import settings
from django.db.utils import IntegrityError
from django.db.models.signals import (pre_save, post_save, post_delete)
from django.dispatch import receiver
from django_common.auth_backends import User

from meta_info.models import Tag
from authentication.models import (Profile, ContactMethod)
from authentication.models_circles import (Circle, Invitation)
from meta_info.models import MetaInfo

from rest_framework.authtoken.models import Token


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Circle)
@receiver(pre_save, sender=Invitation)
@receiver(pre_save, sender=ContactMethod)
@receiver(pre_save, sender=Profile)
def pre_save_instance_create_meta_info(sender, instance, *args, **kwargs):
    """Create a MetaInfo object for the instance being created."""
    if instance.pk:
        return
    if not instance.meta_info:
        instance.meta_info = MetaInfo.objects.create()


@receiver(pre_save, sender=Circle)
def pre_save_circle_create(sender, instance, *args, **kwargs):
    """Circle creation initialise first administrator of the Circle."""
    if instance.pk:
        return
    Invitation.objects.create(
        profile=instance.profile,
        profile_to=instance.profile,
        circle=instance,
        status=Invitation.STATUSES.elevated,
    )


@receiver(post_delete, sender=Invitation)
def post_delete_inviation(sender, instance, *args, **kwargs):
    """set the status of the instance."""
    instance.status = Invitation.STATUSES.withdrawn
    instance.save()


@receiver(pre_save, sender=ContactMethod)
def pre_save_contact_method(sender, instance, *args, **kwargs):
    """Assign fields expected for ContactMethod."""
    if instance.type == ContactMethod.TYPES.email and not instance.email:
        instance.email = instance.detail


@receiver(post_save, sender=ContactMethod)
def post_save_contact_method(sender, instance, *args, **kwargs):
    """Set by default the primary tag for ContactMethod."""
    primary_copy = 'Primary'
    require_primary = [
        ContactMethod.TYPES.email,
        ContactMethod.TYPES.mobile
    ]
    if instance.type in require_primary:
        contacts = ContactMethod.objects.filter(
            profile=instance.profile,
            meta_info__tags__slug__iexact=primary_copy,
        ).count()
        tag = Tag.objects.filter(slug__iexact=primary_copy).first()
        if not tag:
            tag = Tag.objects.create(copy=primary_copy)
        if not contacts:
            instance.meta_info.tags.add(tag)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when an user instance is created."""
    if not created:
        return
    profile = Profile(
        user=instance,
        email=instance.email,
    )
    if instance.is_staff:
        profile.type = Profile.TYPES.admin
    if instance.is_superuser:
        profile.type = Profile.TYPES.destroyer
    profile.save()
    contact = ContactMethod(
        type=ContactMethod.TYPES.email,
        detail=instance.email,
        email=instance.email,
        profile=profile,
    )
    contact.save()


@receiver(post_save, sender=User)
def post_save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated."""
    if not instance.profile.name_first and instance.first_name:
        instance.profile.name_first = instance.first_name
    if not instance.profile.name_family and instance.last_name:
        instance.profile.name_family = instance.last_name
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate authentication API token for a created user instance."""
    if created:
        Token.objects.create(user=instance)
