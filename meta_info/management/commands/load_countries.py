"""Command to create default super user."""

import logging

from django.conf import settings
from django.core.management import BaseCommand

from meta_info.models import Tag
from meta_info.models_localisation import LocationTag
from meta_info.data.countries import COUNTRIES


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Load tags from models."""

    help = __doc__

    def handle(self, *args, **options):
        """load models and check for tags to be created."""
        for country in COUNTRIES:
            if LocationTag.objects.filter(iso_alpha_3=country[2]).count():
                continue
            instance = LocationTag.objects.create(
                copy=country[0],
                iso_alpha_2=country[1],
                iso_alpha_3=country[2],
                iso_numeric=country[3],
            )
            default_location = settings.DEFAULT_LOCATION.lower()
            if instance.iso_alpha_3.lower() is default_location:
                tag = Tag.objects.get_or_create_tag('Default')
                instance.tags.set([tag])
            logger.info('Added Location Tag: {}'.format(country[2]))
