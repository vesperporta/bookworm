"""Books models."""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from bookworm.mixins_publishable import PublishableModelMixin
from meta_info.models import MetaInfo
from posts.exceptions import (
    InvalidEmoteModification,
    DuplicateEmoteValidationError,
    UnemoteValidationError,
)


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
        related_name='emoted+',
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
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def emote_aggregation(self):
        """Aggregation of emotes for printability."""
        return [
            [Emote.EMOTES[k], v] for k, v in enumerate(self.emote_aggregate)
        ]

    def _emote_aggregation_update(
            self,
            index=None,
            adding=True,
            save_obj=False,
    ):
        """Aggregate values for an object to keep data synced."""
        all_emotes = self.emotes.all()
        aggregate = [0] * len(Emote.EMOTES)
        for item in all_emotes:
            aggregate[item[0]] += 1
        if index is not None:
            aggregate[index] += 1 if adding else -1
            if aggregate[index] < 0:
                raise InvalidEmoteModification(item, self)
        self.emote_aggregate = aggregate
        if save_obj:
            self.save()

    def has_emoted(self, profile):
        """Check if the profile has emoted with this model."""
        return self.emotes.filter(profile__id=profile.id).first()

    def emoted(self, emote_type, profile):
        """Add an Emote to this model."""
        if self.has_emoted(profile):
            raise DuplicateEmoteValidationError(profile, self)
        emote = Emote.objects.create(
            type=emote_type,
            profile=profile,
        )
        self.emotes.add(emote)
        self._emote_aggregation_update(emote_type, adding=True)
        self.save()

    def demote(self, profile):
        """Remove an Emote from this model."""
        emote = self.has_emoted(profile)
        if not emote:
            raise UnemoteValidationError(profile, self)
        emote_type = emote.type
        self.emotes.remove(emote)
        emote.delete()
        self._emote_aggregation_update(emote_type, adding=False)
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
    parent = models.ForeignKey(
        'posts.Post',
        related_name='children',
        verbose_name=_('Parent Post'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='posts+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Title and author of book."""
        return f'{self.profile.display_name} posted {self.id}:{self.copy[:30]}'
