import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class DuplicateInvitationValidationError(ValidationError):

    def __init__(self, target, invite):
        super().__init__([{
            'code': 'duplicate_invitation_validation_error',
            'message': f'{target} already has an invite for '
                       f'{invite.profile_to.display_name} from '
                       f'{invite.profile.display_name}.',
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


class InvitationMissingError(ValidationError):

    def __init__(self, target, profile_to):
        super().__init__([{
            'code': 'invitation_missing_error',
            'message': f'{target} has no invitation for '
                       f'{profile_to.display_name}.',
        }])
        logger.error(self)
