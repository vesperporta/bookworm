import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class InvalidEmoteModification(ValidationError):

    def __init__(self, emoted, changed):
        super().__init__({
            'code': 'emote_aggregate_invalid',
            'message': f'Invalid change in Emote({emoted}) '
                       f'aggregation on {changed}!',
        })
        logger.error(self)


class DuplicateEmoteValidationError(ValidationError):

    def __init__(self, profile, target):
        super().__init__({
            'code': 'duplicate_emote_validation_error',
            'message': f'Profile:{profile} has already emoted on {target}',
        })
        logger.error(self)


class UnemoteValidationError(ValidationError):

    def __init__(self, profile, target):
        super().__init__({
            'code': 'unemote_validation_error',
            'message': f'Profile:{profile} had not emoted on {target}',
        })
        logger.error(self)
