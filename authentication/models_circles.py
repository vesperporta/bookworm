"""Profile models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import MetaInfo, MetaInfoMixin
from authentication.models import ContactMethod, Profile
from authentication.models_token import Token
from authentication.exceptions import (
    DuplicateInvitationValidationError,
    InvitationValidationError,
    InvitationMissingError,
    CircleDomainAlreadyVerifiedError,
    CircleDomainTokenNotExistError,
    CircleDomainInProgressError,
)


class Invitation(PreserveModelMixin, ProfileReferredMixin):
    """Invitation object to link two profiles for an object.

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
        salt=settings.SALT_AUTHENTICATION_INVITATION,
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
        """Check the unique togetherness of the two profiles.

        @param profile_to: Profile invited to this object.

        @return Invitation or None
        """
        return self.invites.filter(profile_to__id=profile_to.id).first()

    def _validate_invite_status_change(
            self,
            status_to,
            profile_from,
            profile_to
    ):
        """Validate a change for Invitation objects.

        Rules of validation are laid out as code comments: `Rule #: ...`.

        @param status_to: Int determining the desired invite status.
        @param profile_from: Profile of user making the request.
        @param profile_to: Profile invited to object.

        @return bool

        @raises InvitationValidationError on validation failure.
        """
        # Rule 1: Profile of self can do anything.
        if hasattr(self, 'profile') and self.profile == profile_from:
            return True
        profile_from_invite = self.invites.filter(profile=profile_from).first()
        elevated_action_list = [
            Invitation.STATUSES.banned,
            Invitation.STATUSES.rejected,
        ]
        # Rule 2: profile_from.status above accepted status can ban or reject.
        if (
            profile_from_invite and
            profile_from_invite.status > Invitation.STATUSES.accepted and
            status_to in elevated_action_list
        ):
            return True
        # Rule 3: Invited profile can withdraw.
        if (
            self.invites.filter(
                profile_to=profile_to,
                status=Invitation.STATUSES.invited,
            ).first() and
            profile_from == profile_to and
            status_to == Invitation.STATUSES.withdrawn
        ):
            return True
        # Failure to comply with rules exception.
        raise InvitationValidationError(
            self,
            status_to,
            profile_from,
            profile_to,
        )

    def invite(self, profile, profile_to, status=Invitation.STATUSES.invited):
        """Create an Invitation between teh two profiles and assign.

        @param profile: Profile inviting profile_to.
        @param profile_to: Profile being invited to this object.
        @param status: Int defaults to 3 as invited.

        @return Invitation

        @raises DuplicateInvitationValidationError
        """
        invite = self.has_invited(profile_to)
        if invite:
            raise DuplicateInvitationValidationError(self, invite)
        if hasattr(self, 'invite_same_domain'):
            if self.invite_same_domain.verified:
                pass
        self._validate_invite_status_change(status, profile, profile_to)
        invite = Invitation.objects.create(
            profile=profile,
            profile_to=profile_to,
            status=status,
        )
        self.invites.add(invite)
        return invite

    def invite_change(self, profile, profile_to, status):
        """Change an Invitation between two profiles.

        @param profile: Profile inviting profile_to.
        @param profile_to: Profile being invited to this object.
        @param status: Int defaults to 3 as invited.

        @return Invitation

        @raises InvitationMissingError
        """
        invite = self.has_invited(profile_to)
        if not invite:
            raise InvitationMissingError(self, profile_to)
        self._validate_invite_status_change(status, profile, profile_to)
        invite.status = status
        invite.save()
        return invite

    @property
    def invites_count(self):
        """Number of Profiles accepted into Circle."""
        status_list = [
            Invitation.STATUSES.accepted,
            Invitation.STATUSES.elevated,
        ]
        return self.invites.filter(status__in=status_list).count()


class Circle(Invitable, PreserveModelMixin):
    """Profile and group relationship model."""

    PREFIX = '¶'  # Pilcrow

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_CIRCLE,
    )
    title = models.CharField(
        verbose_name=_('Reading Circle Title'),
        max_length=254,
        db_index=True,
    )
    invite_same_domain = models.ForeignKey(
        Token,
        related_name='circles+',
        verbose_name=_('Verified domain token'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
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

    class Meta:
        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    def __str__(self):
        """String representation of this model."""
        return f'Circle({self.PREFIX}{self.id}-{self.title})'

    def create_verified_token(self, profile):
        if self.verified_token:
            if self.verified_token.validated:
                raise CircleDomainAlreadyVerifiedError(self)
            raise CircleDomainInProgressError(self)
        domain = profile.email.split('@')[1]
        self.invites.filter(profile_to__email__icontains=domain)
        self.verified_token = Token.create(f'{self.id}#{profile.email}')
        self.save()

    def verify_domain(self, token):
        if not self.verified_token:
            raise CircleDomainTokenNotExistError(self)
        elif self.verified_token.validated:
            raise CircleDomainAlreadyVerifiedError(self)
        validated = self.verified_token.validate(token)
        return validated

    @staticmethod
    def create(profile, **kwargs):
        circle = Circle.objects.create(**kwargs)
        Invitation.objects.create(
            profile=profile,
            profile_to=profile,
            circle=circle,
            status=Invitation.STATUSES.elevated,
        )


class CircleSetting(PreserveModelMixin, MetaInfoMixin):
    """Circle Settings model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_CIRCLESETTING,
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
        return f'CircleSetting({self.id}: {Circle.PREFIX}{self.circle.id})'
