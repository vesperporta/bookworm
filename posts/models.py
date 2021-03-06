"""Books models."""

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from meta_info.models import MetaInfo
from meta_info.models_localisation import Localisable
from file_store.models import Imagable
from posts.exceptions import (
    InvalidEmoteModification,
    DuplicateEmoteValidationError,
    UnemoteValidationError,
)


class Emote(PreserveModelMixin, ProfileReferredMixin):
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
        salt=settings.SALT_POSTS_EMOTE,
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

    def _emote_aggregation_update(self):
        """Aggregate values for an object to keep data synced, without DB."""
        all_emotes = self.emotes.filter(deleted_at__isnull=True)
        aggregate = [0] * len(Emote.EMOTES)
        for item in all_emotes:
            aggregate[int(item.type)] += 1
        self.emote_aggregate = aggregate
        self.save()

    def has_emoted(self, profile):
        """Check if the profile has emoted with this model.

        @param profile: Profile of the Emote.

        @return Emote or None
        """
        return self.emotes.filter(
            profile=profile,
            deleted_at__isnull=True,
        ).first()

    def emoted(self, emote_type, profile):
        """Add an Emote to this model.

        @param emote_type: Int type of Emote.
        @param profile: Profile of user emoting.

        @return Emote

        @raises DuplicateEmoteValidationError
        """
        emote = self.has_emoted(profile)
        if emote:
            if emote.type == emote_type:
                raise DuplicateEmoteValidationError(profile, self)
            emote.delete()
        emote = Emote.objects.create(
            type=emote_type,
            profile=profile,
        )
        self.emotes.add(emote)
        self._emote_aggregation_update()
        return emote

    def un_emote(self, profile):
        """Remove an Emote from this model.

        @param profile: Profile of user removing their Emote.

        @return Emote removed from object.

        @raises UnemoteValidationError
        """
        emote = self.has_emoted(profile)
        if not emote:
            raise UnemoteValidationError(profile, self)
        emote.delete()
        self._emote_aggregation_update()
        return emote


class Post(
        Emotable,
        Localisable,
        Imagable,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Post model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_POSTS_POST,
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
