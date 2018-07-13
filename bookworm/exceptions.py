import logging

from django.db import IntegrityError
from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class OperationReservedInternally(ValidationError):

    def __init__(self, current_user):
        super().__init__({
            'code': 'unexpected_user',
            'message': '{}, get realz!'.format(
                current_user.profile.display_name
            ),
        })
        logger.error(self)


class InvalidOperation(ValidationError):

    def __init__(self, obj):
        super().__init__({
            'code': 'invalid_operation',
            'message': '{}, nopez!'.format(obj),
        })
        logger.error(self)


class PublishableObjectNotDefined(ValidationError):

    def __init__(self, attempted_instance, action='publish'):
        super().__init__({
            'code': 'publishable_class_undefined',
            'message': '{} {} attempt without `Publishable` info.'.format(
                attempted_instance.__class__,
                action,
            ),
        })
        logger.error(self)


class PublishableValidationError(ValidationError):

    def __init__(self, attempted_instance, errors):
        super().__init__({
            'code': 'publishable_class_undefined',
            'message': '{} invalid publish attempt.'.format(
                attempted_instance.__class__,
            ),
            'errors': errors,
        })
        logger.error(self)


class NoPublishedDataError(ValidationError):

    def __init__(self, attempted_instance):
        super().__init__({
            'code': 'publishable_not_published',
            'message': f'{attempted_instance} invalid publish attempt.',
        })
        logger.error(self)


class DataMissingValidationError(ValidationError):

    def __init__(self, object, key_1, key_2):
        super().__init__({
            'code': 'missing_values_forbidden',
            'message': '{}:{} and {}:{}'
                    ', at least one value expected!'.format(
                        '{}.{}'.format(str(object), key_1),
                        getattr(object, key_1),
                        '{}.{}'.format(str(object), key_2),
                        getattr(object, key_2),
                    ),
        })
        logger.error(self)


class DataDuplicationIntegrityError(IntegrityError):

    def __init__(self, object, key_1, key_2):
        super().__init__({
            'code': 'duplicate_values_forbidden',
            'message': '{}:{} and {}:{}'
                    ', are forbidden to be identical!'.format(
                        '{}.{}'.format(str(object), key_1),
                        getattr(object, key_1),
                        '{}.{}'.format(str(object), key_2),
                        getattr(object, key_2),
                    ),
        })
        logger.error(self)


class DataMissingIntegrityError(IntegrityError):

    def __init__(self, object, key_1, key_2):
        super().__init__({
            'code': 'missing_values_forbidden',
            'message': '{}:{} and {}:{}'
                    ', at least one value expected!'.format(
                        '{}.{}'.format(str(object), key_1),
                        getattr(object, key_1),
                        '{}.{}'.format(str(object), key_2),
                        getattr(object, key_2),
                    ),
        })
        logger.error(self)


class PublishedUnauthorisedValidation(ValidationError):

    def __init__(self, access_from):
        super().__init__({
            'code': 'published_access_unauthorised_validation',
            'message': f'Object {access_from} not authorised.',
        })
        logger.error(self)
