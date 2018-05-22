"""Books models."""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (
    PublishableModelMixin, ProfileReferredMixin, PreserveModelMixin
)
from meta_info.models import MetaInfo
from posts.exceptions import InvalidEmoteModification


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

    id = HashidAutoField(
        primary_key=True,
        salt='cioP>D^|E*21?"R5&.)rg[8,W@76+VUu',
    )
    type = models.IntegerField(
        choices=EMOTES,
    )

    class Meta:
        verbose_name = 'Emote'
        verbose_name_plural = 'Emotes'

    def __str__(self):
        """Display only as URI valid slug."""
        return f'{Emote.EMOTES[self.type]}{self.profile.display_name}'


class Emotable(models.Model):
    """Mixin to Emotes for models."""

    emotes = models.ManyToManyField(
        Emote,
        related_name='emoted',
        verbose_name=_('Emotes'),
        blank=True,
    )
    emote_aggregate = ArrayField(
        verbose_name=_('Emote Aggregate'),
        base_field=models.IntegerField(
            blank=True,
        ),
        size=8,
        blank=True,
    )

    class Meta:
        abstract = True

    @property
    def emote_aggregation(self):
        """Aggregation of emotes for printability."""
        return [
            [Emote.EMOTES[k], v] for k, v in enumerate(self.emote_aggregate)
        ]

    def _modify_emote_aggregation(self, index, adding=True):
        """Change the aggregate score without needing to save model twice."""
        aggregate_score = self.emote_aggregate[index]
        if adding:
            aggregate_score += 1
        else:
            aggregate_score -= 1
            if aggregate_score < 0:
                raise InvalidEmoteModification(Emote.EMOTES[index], self)
        self.emote_aggregate[index] = aggregate_score

    def has_emoted(self, profile):
        """Check if the profile has emoted with this model."""
        return self.emotes.filter(profile__id=profile.id).first()

    def emoted(self, emote_type, profile):
        """Add an Emote to this model."""
        if self.has_emoted(profile):
            return
        emote = Emote.objects.create(
            type=emote_type,
            profile=profile,
        )
        self.emotes.add(emote)
        self._modify_emote_aggregation(emote_type, adding=True)
        self.save()

    def demote(self, profile):
        """Remove an Emote from this model."""
        emote = self.has_emoted(profile)
        if not emote:
            return
        emote_type = emote.type
        self.emotes.remove(emote)
        emote.delete()
        self._modify_emote_aggregation(emote_type, adding=False)
        self.save()


class Post(
        PublishableModelMixin,
        Emotable,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Post model."""

    id = HashidAutoField(
        primary_key=True,
        salt='g5t|Q)XG3%$@fen9UlE4:BShuqW=]jH2',
    )
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
        Emotable,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Comment model."""

    id = HashidAutoField(
        primary_key=True,
        salt='e(2W,>JajbvtM4pzUlc@B=$1+hI;g3/8',
    )
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
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'

    def __str__(self):
        """Title and author of book."""
        return '{} says {}'.format(self.profile, self.copy)
