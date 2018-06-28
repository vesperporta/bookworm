"""Meta Information models."""

import logging
import hashlib
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hashid_field import HashidAutoField

from meta_info.models import TagMixin
from bookworm.mixins import PreserveModelMixin
from meta_info.exceptions import (
    LocalisationNoFieldException,
    LocalisationUnknownLocaleException,
)


logger = logging.getLogger(__name__)


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
            self.iso_639_1.lower() == settings.DEFAULT_LANGUAGE.lower()
        )

    def __str__(self):
        """ISO and name of language."""
        return 'LanguageTag({} "{}")'.format(self.iso_639_1, self.copy[:30])


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
            self.iso_alpha_2.lower() == settings.DEFAULT_LOCATION.lower()
        )

    def __str__(self):
        """ISO and name of location."""
        return 'LocationTag({} "{}")'.format(self.iso_alpha_2, self.copy[:30])


class LocaliseTag(PreserveModelMixin):
    """Localisation Tag for translation assistance."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_LOCALISETAG,
    )
    field_name = models.CharField(
        verbose_name=_('Models field name'),
        max_length=256,
        blank=True,
    )
    copy = models.TextField(
        verbose_name=_('Translated Copy'),
    )
    original = models.CharField(
        verbose_name=_('Hash of source'),
        max_length=256,
        blank=True,
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

    @staticmethod
    def locale_from_code(self, localise_code=settings.DEFAULT_LOCALISATION):
        """Convert a localisation code '{language}-{location}' to objects.

        Example for a code: 'en-gb', which would be split into two objects
        - 'en' would evaluate to a LanguageTag object.
        - 'gb' would evaluate to a LocationTag object.

        @param localise_code: Str code

        @return LanguageTag, LocationTag, Str

        Third return value is the Str code used to find locale.
        """
        codes = localise_code.lower().split('-')
        language = LanguageTag.objects.filter(
            iso_639_1__iexact=codes[0],
        ).first()
        location = LocationTag.objects.filter(
            iso_alpha_2__iexact=codes[1],
        ).first()
        if not language and not location:
            raise LocalisationUnknownLocaleException(
                localise_code,
                language,
                location,
            )
        return language, location, localise_code

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
        language = self.language.iso_639_1.lower()
        location = self.location.iso_alpha_2.lower()
        return f'{language}-{location}'

    def __str__(self):
        """ISO codes of language and location."""
        return f'LocaliseTag({self.display_code})'


class Localisable(models.Model):
    """Mixin for localisation ability."""

    localisations = models.ManyToManyField(
        LocaliseTag,
        related_name='localised+',
        verbose_name=_('Localisation'),
        blank=True,
    )

    class Meta:
        abstract = True

    def localise(
            self,
            field_name,
            localised_value,
            localise_code=settings.DEFAULT_LOCALISATION,
            force=False,
    ):
        """Store a localised field value for this object.

        @param field_name: Str parameter name of this object.
        @param localised_value: Str value of localisation.
        @param localise_code: Str code of localisation.
        @param force: Bool, default = False, overwrite existing localisation.

        @raises LocalisationNoFieldException
        @raises LocalisationUnknownLocaleException
        """
        if not hasattr(self, field_name):
            raise LocalisationNoFieldException(self, field_name)
        original_value = getattr(self, field_name)
        original_hash = hashlib.md5(original_value.encode('utf-8')).hexdigest()
        language, location = LocaliseTag.locale_from_code(localise_code)
        localisation = self.localisations.filter(
            field_name=field_name,
            language=language,
            Location=location,
        ).first()
        if localisation:
            if localisation.original == original_hash and not force:
                logger.info(
                    f'Localisation already exists as {localisation.id}, '
                    f'field_name: {field_name}, code: {localise_code}.',
                )
                return
            localisation.delete()
            self.localisations.remove(localisation)
        self.localisations.add(
            LocaliseTag.objects.create(
                field_name=field_name,
                copy=localised_value,
                original=original_hash,
                language=language,
                location=location,
            )
        )

    def locale_value(
            self,
            field_name,
            localise_code=settings.DEFAULT_LOCALISATION,
    ):
        """Find the localised value for a field.

        @param field_name: Str parameter name of this object.
        @param localise_code: Str code of localisation.

        @return Str or None

        @raises LocalisationNoFieldException
        """
        if not hasattr(self, field_name):
            raise LocalisationNoFieldException(self, field_name)
        language, location = LocaliseTag.locale_from_code(localise_code)
        localised = self.localisations.filter(
            field_name__iexact=field_name,
            language=language,
            location=location,
        ).first()
        return localised.copy if localised else None

    def locale_as(self, localise_code):
        """Detail this objects localisations according to the code supplied.

        To assist in JSON values being transcribed correctly for numbers
        and boolean values there are basic checks to support these value types.

        @:param localise_code: str representation of the localisation.

        @:return dict with all localised fields.
        """
        language, location = LocaliseTag.locale_from_code(localise_code)
        localised = self.localisations.filter(
            language=language,
            location=location,
        )
        return_dict = {}
        for locale in list(localised):
            locale_value = locale.copy
            if type(getattr(self, locale.field_name)) is models.IntField:
                locale_value = int(locale_value)
            if type(getattr(self, locale.field_name)) is models.FloatField:
                locale_value = float(locale_value)
            if type(getattr(self, locale.field_name)) is models.DecimalField:
                locale_value = Decimal(locale_value)
            if type(getattr(self, locale.field_name)) in [
                models.BooleanField,
                models.NullBooleanField,
            ]:
                locale_value = bool(locale_value)
            return_dict.update({locale.field_name: locale_value, })
        return return_dict
