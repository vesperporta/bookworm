"""Authentication JWT serializers."""

from django.contrib.auth import authenticate
from django_common.auth_backends import User
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UsernameEmailJWTSerializer(JSONWebTokenSerializer):
    """Username and Email user identifier JWT token serializer."""

    def validate(self, attrs):
        """Validates the supplied username for an email to identify a User.

        @:param attrs: dict supplied fields from request.

        @:returns dict

        @:raises ValidationError
        """
        username = attrs.get(self.username_field)
        try:
            if username.index('@') > -1:
                user_obj = User.objects.filter(
                    email=attrs.get(self.username_field)
                ).first()
                username = user_obj.username
        except ValueError:
            pass
        credentials = {
            'username': username,
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                payload = jwt_payload_handler(user)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
