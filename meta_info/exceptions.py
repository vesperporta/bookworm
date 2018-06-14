import logging

from rest_framework.serializers import ValidationError


logger = logging.getLogger(__name__)


class LocalisationNoFieldException(ValidationError):

    def __init__(self, target, field_name):
        super().__init__([{
            'code': 'localisation_validation_no_field_exception',
            'message': f'{target} has no field of name {field_name}.',
        }])
        logger.error(self)


class LocalisationUnknownLocaleException(ValidationError):

    def __init__(self, localise_code, language, location):
        super().__init__([{
            'code': 'localisation_validation_unknown_locale_exception',
            'message': f'No localisation known for the code {localise_code}.'
                       f' Language: {language}, Location: {location}.',
        }])
        logger.error(self)
