"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.exceptions import DataMissingIntegrityError
from bookworm.mixins import (
    PublishableModelMixin, ProfileReferredMixin, PreserveModelMixin
)
from meta_info.models import MetaInfo


class Post(
        PublishableModelMixin,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Post model."""

    id = HashidAutoField(primary_key=True)
    copy = models.TextField(
        verbose_name=_('Post copy'),
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='posts+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = ('comments', )
        # serializer = PublishBookSerializer

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Title and author of book."""
        return '{} posted {}'.format(self.profile, self.copy)


class Comment(
        PublishableModelMixin,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Comment model."""

    id = HashidAutoField(primary_key=True)
    copy = models.CharField(
        verbose_name=_('Comment copy'),
        max_length=400,
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        verbose_name=_('Posting'),
        on_delete=models.DO_NOTHING,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='posts+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = None
        # serializer = PublishBookSerializer

    class Meta:
        verbose_name = 'Posts\' Comment'
        verbose_name_plural = 'Posts\' Comments'

    def __str__(self):
        """Title and author of book."""
        return '{} says {}'.format(self.profile, self.copy)


class Emote(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Emote model."""

    EMOTES = Choices(
        (0, 'thrill', _('👓')),
        (1, 'heart', _('❤️')),
        (2, 'joy', _('😂')),
        (3, 'annoy', _('💀')),
        (4, 'rubbish', _('💩')),
        (5, 'confused', _('😕')),
        (6, 'block', _('🤬')),
    )

    id = HashidAutoField(primary_key=True)
    type = models.IntegerField(
        choices=EMOTES,
    )
    post = models.ForeignKey(
        Post,
        related_name='emotes',
        verbose_name=_('Posting'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    comment = models.ForeignKey(
        Comment,
        related_name='emotes',
        verbose_name=_('Comment'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Emote'
        verbose_name_plural = 'Emotes'
        unique_together = (
            ('profile', 'post', ),
            ('profile', 'comment', ),
        )

    def save(self):
        if not self.post and not self.comment:
            raise DataMissingIntegrityError(self, 'post', 'comment')
        return super().save()

    def __str__(self):
        """Display only as URI valid slug."""
        return '{} {} "{}"'.format(
            self.profile,
            Emote.EMOTES[self.type],
            self.book if self.book else self.comment,
        )
