"""Profile models."""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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
    InvitationAlreadyVerifiedError,
    InvitationTokenNotExistError,
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
    token = models.ForeignKey(
        Token,
        related_name='circles+',
        verbose_name=_('Verified domain token'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
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

    def token_recreate(self):
        """Generate a new token for this invite.

        @:raises InvitationAlreadyVerifiedError
        """
        if self.token and self.token.validated:
            raise InvitationAlreadyVerifiedError(self)
        self.token = Token.objects.create_token(f'{self.id}#{profile_to.email}')

    def token_verify(self, token_value):
        """Validate a token with a supplied value.

        @:param token_value: str supplied for validation.

        @:return bool

        @:raises InvitationTokenNotExistError
        @:raises InvitationAlreadyVerifiedError
        """
        if not self.token:
            raise InvitationTokenNotExistError(self)
        elif self.token.validated:
            raise InvitationAlreadyVerifiedError(self)
        return self.token.validate(token_value)


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

    def _invite_validate_status_change(
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
        elevated_action_list = [
            Invitation.STATUSES.banned,
            Invitation.STATUSES.rejected,
        ]
        # Rule 1: Profile of self can do anything.
        if hasattr(self, 'profile') and self.profile == profile_from:
            return True
        profile_to_invite = self.invites.filter(profile_to=profile_to).first()
        # Rule 2: Self-invites `profile_from=None` can only create.
        if (
            not profile_from and
            status_to == Invitation.STATUSES.invited and
            not profile_to_invite
        ):
            return True
        # Rule 3: profile_from.status above accepted status can ban or reject.
        if (
            profile_to_invite and profile_to_invite.profile == profile_from and
            profile_to_invite.status > Invitation.STATUSES.accepted and
            status_to in elevated_action_list
        ):
            return True
        # Rule 4: Invited profile can withdraw.
        if (
            profile_to_invite.status == Invitation.STATUSES.invited and
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
        """Create an Invitation between two profiles and assign.

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
        self._invite_validate_status_change(status, profile, profile_to)
        time_delta = timedelta(
            days=settings.INVITE_TIMEOUT) if profile else timedelta(
            days=settings.INVITE_SELF_TIMEOUT)
        invite = Invitation.objects.create(
            profile=profile,
            profile_to=profile_to,
            status=status,
            token=Token.objects.create_token(
                f'{self.id}#{profile_to.email}',
                expiry=timezone.now() + time_delta,
            ),
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
        self._invite_validate_status_change(status, profile, profile_to)
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

    @staticmethod
    def create(profile, **kwargs):
        """Create a new Circle object with the creator as an elevated owner.

        @:param profile: Profile of the owner of the new Circle.
        @:param **kwargs: values defined required for creation of a Circle.

        @:return Circle
        """
        token = Token.objects.create_token(
            f'original#{profile.email}',
            token_value=Token.objects.generate_sha256(profile.email),
        )
        invite = Invitation.objects.create(
            profile=profile,
            profile_to=profile,
            status=Invitation.STATUSES.elevated,
            token=token,
        )
        circle = Circle.objects.create(**kwargs, invites=[invite])
        token.validated = True
        token.expiry = timezone.now()
        token.save()
        return circle


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
