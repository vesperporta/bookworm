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


class BookDoesNotExistException(ValidationError):

    def __init__(self, param):
        super().__init__({
            'code': 'book_does_not_exist_error',
            'message': f'Book of id {param}, does not exist.',
        })
        logger.error(self)


class AnswerAlreadyAcceptedValidation(ValidationError):

    def __init__(self, profile_accepted):
        super().__init__({
            'code': 'read_answer_already_accepted_validation',
            'message': f'Answer already accepted by: '
                       f'{profile_accepted.display_name}.',
        })
        logger.error(self)


class CannotAcceptOwnAnswerValidation(ValidationError):

    def __init__(self):
        super().__init__({
            'code': 'cannot_accept_own_answer_validation',
            'message': f'Accepting your own answer, 😂.',
        })
        logger.error(self)
