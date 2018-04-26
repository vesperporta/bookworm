"""Books app serializers."""

from rest_framework import serializers

from hashid_field import rest

from bookworm.exceptions import InvalidOperation
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
from authentication.models import (
    Profile,
    ContactMethod,
)
from authentication.models_circles import (
    Circle,
    Invitation,
)


class ContactMethodSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    id = rest.HashidSerializerCharField(read_only=True)

    class Meta:
        model = ContactMethod
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'meta_info',
        )
        fields = (
            'detail',
            'email',
        )
        exclude = []


class ProfileSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    id = rest.HashidSerializerCharField(read_only=True)

    class Meta:
        model = Profile
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'name_title',
            'name_first',
            'name_family',
            'name_middle',
            'birth_date',
            'invitations',
        )
        exclude = []


class CircleSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    id = rest.HashidSerializerCharField(read_only=True)

    class Meta:
        model = Circle
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'created_by',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'reading_list',
            'invitations',
        )
        exclude = []


class InvitationSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    id = rest.HashidSerializerCharField(read_only=True)

    class Meta:
        model = Invitation
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'status',
            'profile_to',
            'circle',
        )
        exclude = []

    def validate(self, data):
        """Validate for profile assignment to validated_data"""
        current_user = self.context['request'].user
        if current_user.id == data['profile_to']:
            raise InvalidOperation(self)
        return super().validate(data)
