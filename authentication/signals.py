"""Profile signals."""

import logging

from django.conf import settings
from django.db.models.signals import (pre_save, post_save, post_delete)
from django.dispatch import receiver
from django_common.auth_backends import User

from meta_info.models import Tag
from authentication.models import (Profile, ContactMethod)
from authentication.models_circles import Invitation

from rest_framework.authtoken.models import Token


logger = logging.getLogger(__name__)


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
    """Set b y default the primary tag for ContactMethod."""
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
        try:
            tag = Tag.objects.get(slug=primary_copy)
        except Exception:
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
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate authentication API token for a created user instance."""
    if created:
        Token.objects.create(user=instance)
