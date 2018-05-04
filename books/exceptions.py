import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class UnknownThrillAssociation(ValidationError):

    def __init__(self, thrill):
        super().__init__([{
            'code': 'thrill_association_unknown',
            'message': f'Thrill: {thrill.id}, has no association!',
        }])
        logger.error(self)
