"""Command to create default super user."""

import logging

from django.core.management import BaseCommand
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """create a default super user."""

    help = __doc__

    def handle(self, *args, **options):
        """Create default super user."""
        if not User.objects.filter(username='root').first():
            user = User.objects.create_superuser(
                'root',
                'root@admin.com',
                'iamsosecret',
            )
            logger.info('Default super user created: {}'.format(user.username))
        else:
            logger.warn('Default super user already exists')
        if not User.objects.filter(username='vesperporta').first():
            user = User.objects.create_user(
                'vesperporta',
                'vesper.porta@gmail.com',
                ']&=9r|*<<4?{3K.#-64{h=r%"|f[<0Tf',
            )
            user.set_unusable_password()
            logger.info('Default user created: {}'.format(user.username))
        else:
            logger.warn('Default user already exists')
