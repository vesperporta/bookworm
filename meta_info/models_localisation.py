"""Meta Information models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from meta_info.models import TagMixin
from bookworm.mixins import PreserveModelMixin


TAGS = (
    'Default',
)


class LanguageTag(TagMixin, PreserveModelMixin):
    """Language object."""

    family = models.TextField(
        blank=True,
    )
    name_native = models.TextField(
        blank=True,
    )
    iso_639_1 = models.CharField(
        max_length=2,
        blank=True,
    )
    iso_639_2_t = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_639_2_b = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_639_3 = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_639_3_original = models.CharField(
        max_length=9,
        db_index=True,
    )
    notes = models.TextField(
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = 'Language Tag'
        verbose_name_plural = 'Language Tags'

    def __str__(self):
        """ISO and name of language."""
        return '{} "{}"'.format(self.iso_639_3, self.copy[:30])


class LocationTag(TagMixin, PreserveModelMixin):
    """Language object."""

    iso_alpha_2 = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_alpha_3 = models.CharField(
        max_length=3,
        db_index=True,
    )
    iso_numeric = models.PositiveIntegerField(
        blank=True,
    )
    parent_location = models.ForeignKey(
        'LocationTag',
        related_name='child_locations+',
        verbose_name=_('Parent Location'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    default_language = models.ForeignKey(
        LanguageTag,
        related_name='default_location_language+',
        verbose_name=_('Default Location Language'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    # TODO: long_lat  # noqa

    class Meta:
        verbose_name = 'Location Tag'
        verbose_name_plural = 'Location Tags'

    def __str__(self):
        """ISO and name of location."""
        return '{} "{}"'.format(self.iso_alpha_3, self.copy[:30])


class LocaliseTag(PreserveModelMixin):
    """Localisation Tag for translation assistance."""

    id = HashidAutoField(primary_key=True)
    field_name = models.TextField(
        verbose_name=_('Models field name'),
        blank=True,
    )
    copy = models.TextField(
        verbose_name=_('Translated Copy'),
    )
    original = models.TextField(
        verbose_name=_('Source replication on archive'),
        blank=True,
    )
    dirty = models.BooleanField(
        verbose_name=_('Source Copy Changed'),
        blank=True,
        default=False,
    )
    language = models.ForeignKey(
        LanguageTag,
        related_name='locale_language+',
        verbose_name=_('Localised Language Tag'),
        on_delete=models.DO_NOTHING,
    )
    location = models.ForeignKey(
        LocationTag,
        related_name='locale_language+',
        verbose_name=_('Localised Country Tag'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Localisation Tag'
        verbose_name_plural = 'Localisation Tags'

    @property
    def default_language(self):
        language = LanguageTag.objects.filter(
            tags__slug__iexact='default',
        ).first()
        if not language:
            language = LanguageTag.objects.filter(
                iso_639_3__iexact=settings.DEFAULT_LANGUAGE,
            ).first()
        return language

    @property
    def default_location(self):
        location = LanguageTag.objects.filter(
            tags__slug__iexact='default',
        ).first()
        if not location:
            location = LanguageTag.objects.filter(
                iso_alpha_3__iexact=settings.DEFAULT_LOCATION,
            ).first()
        return location

    @property
    def display_code(self):
        rtn = '{}'.format(self.language.iso_639_3.lower())
        if self.location:
            rtn += '-{}'.format(self.location.iso_alpha_3.lower())
        return rtn

    def __str__(self):
        """ISO codes of language and location."""
        return self.display_code
