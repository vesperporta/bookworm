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

    def __init__(self, target, profile, profile_to):
        super().__init__([{
            'code': 'un_invitation_validation_error',
            'message': f'{target} has no Invitation active '
                       f'from {profile} to {profile_to}',
        }])
        logger.error(self)
