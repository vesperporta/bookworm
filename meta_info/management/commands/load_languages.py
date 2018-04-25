"""Command to create default super user."""

import logging

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import DataError

from meta_info.models import Tag
from meta_info.models_localisation import LanguageTag
from meta_info.data.languages import LANGUAGES


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Load tags from models."""

    help = __doc__

    def handle(self, *args, **options):
        """load models and check for tags to be created."""
        for language in LANGUAGES:
            if LanguageTag.objects.filter(copy=language[1]).count() > 0:
                continue
            iso_639 = language[6]
            try:
                instance = LanguageTag.objects.create(
                    copy=language[1],
                    family=language[0],
                    name_native=language[2],
                    iso_639_1=language[3],
                    iso_639_2_t=language[4],
                    iso_639_2_b=language[5],
                    iso_639_3=iso_639.split(' ')[0],
                    iso_639_3_original=iso_639,
                    notes=language[7],
                )
            except DataError:
                logger.error('Failed Language import: {}'.format(language))
                return
            if instance.iso_639_3.lower() is settings.DEFAULT_LANGUAGE.lower():
                tag = Tag.objects.filter(slug__iexact='default').first()
                if not tag:
                    tag = Tag.objects.create(copy='Default')
                instance.tags.set([tag])
            logger.info('Added Language tag: {}'.format(language[6]))
