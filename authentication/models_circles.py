"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import MetaInfo, MetaInfoMixin
from authentication.models import ContactMethod, Profile


class Invitation(PreserveModelMixin, ProfileReferredMixin):
    """Invitiation between a circle and a Profile.

    The current user requesting the invitation is defined as `self.profile`.
    """

    STATUSES = Choices(
        (0, 'invited', _('Invited')),
        (1, 'accepted', _('Accepted')),
        (2, 'rejected', _('Rejected')),
        (3, 'withdrawn', _('Withdrawn')),
        (4, 'banned', _('Banned')),
        (5, 'elevated', _('Elevated')),
    )

    id = HashidAutoField(
        primary_key=True,
        salt='XF5&39(7cM~,o4JQz6D.{.xbqvE_W4^b',
    )
    status = models.IntegerField(
        choices=STATUSES,
        default=STATUSES.invited,
        blank=True,
    )
    profile_to = models.ForeignKey(
        Profile,
        related_name='invitations',
        verbose_name=_('Profile Invited'),
        on_delete=models.DO_NOTHING,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='invitation_meta+',
        verbose_name=_('Invitation meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'
        unique_together = ('profile', 'profile_to', 'circle', )

    def __str__(self):
        """Short description of what this invitation is intended."""
        addressed = f'to: {self.profile_to}, from: {self.profile}'
        if self.circle:
            return f'{addressed}, for: {self.circle};'
        return f'{addressed};'


class Invitable(models.Model):
    """Invitations based mixins to add support in managing invites."""

    invites = models.ManyToManyField(
        Invitation,
        related_name='invited_to+',
        verbose_name=_('Invitations'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True

    def has_invited(self, profile, profile_to):
        """Check the unique togetherness of the two profiles."""
        # TODO: status check for if there are any
        return self.invites.filter(
            profile__id=profile.id,
            profile_to__id=profile_to.id,
        ).first()

    def invite(self, profile, profile_to):
        """Create an Invitation between teh two profiles and assign."""
        if self.has_invited(profile, profile_to):
            # raise DuplicateEmoteValidationError(profile, self)
            pass
        self.invites.add(Invitation.objects.create(
            profile=profile,
            profile_to=profile_to,
        ))
        self.save()

    def uninvite(self, profile):
        """Find the Invitaiton of the two profiles and remove."""
        invite = self.has_invited(profile)
        if not invite:
            # raise UnemoteValidationError(profile, self)
            pass
        self.emotes.remove(invite)
        invite.delete()
        self.save()


class Circle(PreserveModelMixin):
    """Profile and group relationship model."""

    PREFIX = '¶'  # Pilcrow

    id = HashidAutoField(
        primary_key=True,
        salt='ODB13\'B/A!8]0w?m_7Dt{Li+!:C{-!}E',
    )
    title = models.CharField(
        verbose_name=_('Reading Circle Title'),
        max_length=254,
        db_index=True,
    )
    profile = models.ForeignKey(
        Profile,
        related_name='circles',
        verbose_name=_('Created by'),
        on_delete=models.DO_NOTHING,
    )
    contacts = models.ManyToManyField(
        ContactMethod,
        related_name='circles+',
        verbose_name=_('Contact Methods'),
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='circles_meta+',
        verbose_name=_('Circles meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    reading_list = models.ForeignKey(
        ReadingList,
        related_name='circles',
        verbose_name=_('Reading List'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    @property
    def count(self):
        """Number of Profiles accepted into Circle."""
        status_list = [
            Invitation.STATUSES.accepted,
            Invitation.STATUSES.elevated,
        ]
        return self.invitations.filter(status__in=status_list).count()

    class Meta:
        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    def __str__(self):
        """Valid email output of profile."""
        return f'{self.PREFIX}{self.title or self.id}'


class CircleSetting(
        PreserveModelMixin,
        MetaInfoMixin,
):
    """Circle Settings model."""

    id = HashidAutoField(
        primary_key=True,
        salt='R;aU-Y.v_,nw8O+/2e%sMLy5m$=A6cbC',
    )
    circle = models.ForeignKey(
        Circle,
        related_name='settings',
        verbose_name=_('Settings for Circle'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Circle Setting'
        verbose_name_plural = 'Circle Settings'
