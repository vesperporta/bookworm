"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import MetaInfo, MetaInfoMixin
from authentication.models import ContactMethod, Profile
from authentication.exceptions import (
    DuplicateInvitationValidationError,
    UnInvitationValidationError,
    InvitationValidationError,
)


class Invitation(PreserveModelMixin, ProfileReferredMixin):
    """Invitiation object to link two profiles for an object.

    The current user requesting the invitation is defined as `self.profile`.
    This object is also a representation of authorisation within a group.
    """

    STATUSES = Choices(
        (0, 'banned', _('Banned')),
        (1, 'rejected', _('Rejected')),
        (2, 'withdrawn', _('Withdrawn')),
        (3, 'invited', _('Invited')),
        (4, 'accepted', _('Accepted')),
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
        unique_together = ('profile', 'profile_to', )

    def __str__(self):
        """Short description of what this invitation is intended."""
        return f'Invitation(to: {self.profile_to}, from: {self.profile})'


class Invitable(models.Model):
    """Invitations based mixins to add support in managing invites."""

    invites = models.ManyToManyField(
        Invitation,
        related_name='invited_to+',
        verbose_name=_('Invitations'),
    )

    class Meta:
        abstract = True

    def has_invited(self, profile_to):
        """Check the unique togetherness of the two profiles."""
        # TODO: status check for if there are any
        return self.invites.filter(profile_to__id=profile_to.id).first()

    def _validate_invite_status_change(
            self,
            status_to,
            profile_from,
            profile_to
    ):
        """Validate a change for Invitation objects.

        rules of validation:
        1. profile of self can do anything.
        2. profile_from.status above accepted can ban or reject.
        3. invited profile can withdraw.
        """
        if hasattr(self, 'profile') and self.profile == profile_from:
            return True
        profile_from_invite = self.invites.filter(profile=profile_from).first()
        elevated_action_list = [
            Invitation.STATUSES.banned,
            Invitation.STATUSES.rejected,
        ]
        if (
            profile_from_invite and
            profile_from_invite.status > Invitation.STATUSES.accepted and
            status_to in elevated_action_list
        ):
            return True
        if (
            self.invites.filter(
                profile_to=profile_to,
                status=Invitation.STATUSES.invited,
            ).first() and
            profile_from == profile_to and
            status_to == Invitation.STATUSES.withdrawn
        ):
            return True
        raise InvitationValidationError(
            self,
            status_to,
            profile_from,
            profile_to,
        )

    def invite(self, profile, profile_to, status=Invitation.STATUSES.invited):
        """Create an Invitation between teh two profiles and assign."""
        if self.has_invited(profile_to):
            raise DuplicateInvitationValidationError(self, profile, profile_to)
        self._validate_invite_status_change(status, profile, profile_to)
        self.invites.add(Invitation.objects.create(
            profile=profile,
            profile_to=profile_to,
            status=status,
        ))
        self.save()

    def invite_change(self, profile, profile_to, status):
        """Change an Invitation between two profiles."""
        self._validate_invite_status_change(status, profile, profile_to)
        invite = self.invites.filter(profile_to=profile_to)
        invite.status = status
        invite.save()

    def uninvite(self, profile, profile_to):
        """Find the Invitaiton of the two profiles and remove."""
        invite = self.has_invited(profile_to)
        if not invite:
            raise UnInvitationValidationError(self, profile_to)
        self._validate_invite_status_change(
            Invitation.STATUSES.rejected,
            profile,
            profile_to,
        )
        self.invites.remove(invite)
        invite.status = Invitation.STATUSES.rejected
        invite.save()
        invite.delete()
        self.save()


class Circle(
        Invitable,
        PreserveModelMixin,
):
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
        """String representation of this model."""
        return f'Circle({self.PREFIX}{self.id}-{self.title})'


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

    def __str__(self):
        """String representation of this model."""
        return f'CircleSetting({self.id}: {self.circle.id})'
