import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class DuplicateInvitationValidationError(ValidationError):

    def __init__(self, target, profile, profile_to):
        super().__init__([{
            'code': 'duplicate_invitation_validation_error',
            'message': f'Profile:{profile} has already emoted on {target}',
        }])
        logger.error(self)


class UnInvitationValidationError(ValidationError):

    def __init__(self, target, profile_to):
        super().__init__([{
            'code': 'un_invitation_validation_error',
            'message': f'{target} has no Invitation active for {profile_to}',
        }])
        logger.error(self)


class InvitationValidationError(ValidationError):

    def __init__(self, target, *args):
        super().__init__([{
            'code': 'invitation_validation_error',
            'message': f'{target} has not been provided with required values: '
                       f'{args}',
        }])
        logger.error(self)
