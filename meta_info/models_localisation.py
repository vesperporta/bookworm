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

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_LANGUAGETAG,
    )
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
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    @property
    def default_language(self):
        """Flag detailing this object as the default language."""
        return bool(
            self.tags.filter(slug__iexact='default') or
            self.iso_639_3.lower() == settings.DEFAULT_LANGUAGE.lower()
        )

    def __str__(self):
        """ISO and name of language."""
        return 'LanguageTag({} "{}")'.format(self.iso_639_3, self.copy[:30])


class LocationTag(TagMixin, PreserveModelMixin):
    """Language object."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_LOCATIONTAG,
    )
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
    # TODO: long_lat  # noqa T000

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    @property
    def default_location(self):
        """Flag detailing this object as the default location."""
        return bool(
            self.tags.filter(slug__iexact='default') or
            self.iso_alpha_3.lower() == settings.DEFAULT_LOCATION.lower()
        )

    def __str__(self):
        """ISO and name of location."""
        return 'LocationTag({} "{}")'.format(self.iso_alpha_3, self.copy[:30])


class LocaliseTag(PreserveModelMixin):
    """Localisation Tag for translation assistance."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_LOCALISETAG,
    )
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
        related_name='localisations',
        verbose_name=_('Language Tag'),
        on_delete=models.DO_NOTHING,
    )
    location = models.ForeignKey(
        LocationTag,
        related_name='localisations',
        verbose_name=_('Country Tag'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Localisation'
        verbose_name_plural = 'Localisations'

    @property
    def default_localisation(self):
        """Flag detailing this object as the default localisation."""
        return bool(
            self.language.default_language and
            self.location.default_location
        )

    @property
    def display_code(self):
        """Display code representing a '{language}-{location}' pair."""
        language = self.language.iso_639_3.lower()
        location = self.location.iso_alpha_3.lower()
        return f'{language}-{location}'

    def __str__(self):
        """ISO codes of language and location."""
        return f'LocaliseTag({self.display_code})'
