import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class BookRequiredValidation(ValidationError):

    def __init__(self, param):
        super().__init__({
            'code': 'book_required_validation',
            'message': f'Book parameter required for request: {param}.',
        })
        logger.error(self)
