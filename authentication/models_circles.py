"""Profile models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import ReadingList
from meta_info.models import MetaInfo
from authentication.models import Profile


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
        return '{}{}'.format(self.PREFIX, self.title or self.id)


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
    circle = models.ForeignKey(
        Circle,
        related_name='invitations',
        verbose_name=_('Circle invited to'),
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
        rtn = 'to: {}, by: {}'.format(
            self.profile_to, self.circle if self.circle else self.profile)
        if self.circle:
            rtn += ', for: {}'.format(self.circle)
        return rtn
