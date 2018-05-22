import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class InvalidEmoteModification(ValidationError):

    def __init__(self, emoted, changed):
        super().__init__([{
            'code': 'emote_aggregate_invalid',
            'message': f'Invalid change in Emote({emoted}) '
                       f'aggregation on {changed}!',
        }])
        logger.error(self)
