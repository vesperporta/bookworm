"""Tasks required from authentication service."""

from authentication.models_token import Token
from authentication.serializers import ProfileSerializer


def task_send_message_invitable_action(action_performed, object_actioned):
    """Task expected from Invitable actions to process messages required.

    @:param action_performed: str representation of action.
    @:param object_actioned: object invitable action taken upon.
    """
    pass


def task_reset_user_secret_key(user):
    """Rest authentication token for a users profile.

    @:param user: User object.

    @:returns str
    """
    user.profile.auth_token = Token.objects.create_random()
    user.profile.save()
    return Token.objects.get_value(user.profile.auth_token)


def task_get_user_secret_key(user):
    """Obtain authentication token for a users profile.

    @:param user: User object.

    @:returns str
    """
    if not user.profile.auth_token:
        return task_reset_user_secret_key(user)
    return Token.objects.get_value(user.profile.auth_token)


def jwt_response_payload_handler(token, user=None, request=None):
    """JWT login response with serialized Profile data."""
    return {
        'token': token,
        'profile': ProfileSerializer(
            user.profile,
            context={'request': request},
        ).data
    }
