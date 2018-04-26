"""Serializers to provide generic functionality."""
from rest_framework import serializers

from bookworm.exceptions import OperationReservedInternally
from authentication.models import Profile


class ProfileRefferedSerializerMixin:
    """Manage the creation of an object with reference to a Profile."""
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )

    def validate(self, data):
        """Validate for profile assignment to validated_data"""
        current_user = self.context['request'].user
        if 'profile' not in data:
            data['profile'] = current_user.profile
        elif current_user.id != data['profile']:
            if not current_user.is_superuser and not current_user.is_staff:
                raise OperationReservedInternally(current_user)
        return super().validate(data)


class PreservedModelSerializeMixin:
    """Prevent deletion serializer mixin."""
    created_at = serializers.ReadOnlyField()
    modified_at = serializers.ReadOnlyField()
    deleted_at = serializers.ReadOnlyField()
