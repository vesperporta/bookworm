"""Books app serializers."""

from rest_framework import serializers

from bookworm.exceptions import InvalidOperation
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
from bookworm.serializers import ProfileRefferedSerializerMixin
from authentication.models import (
    Profile,
    Author,
    ContactMethod,
)
from authentication.models_circles import (
    Circle,
    Invitation,
)


class ProfileSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='profile-detail',
    )
    pen_names = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='author-detail',
        queryset=Author.objects.all(),
        required=False,
        allow_null=True,
    )
    contacts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='contactmethod-detail',
        queryset=ContactMethod.objects.all(),
    )
    circles = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='circle-detail',
        queryset=Circle.objects.all(),
    )
    invitations = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='invitation-detail',
    )

    class Meta:
        model = Profile
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'email',
            'type',
        )
        fields = read_only_fields + (
            'name_title',
            'name_first',
            'name_family',
            'name_middle',
            'name_display',
            'birth_date',
            'death_date',
            'pen_names',
            'contacts',
            'circles',
            'invitations',
        )
        exclude = []


class AuthorSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='author-detail',
    )
    contacts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='contactmethod-detail',
        queryset=ContactMethod.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Author
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
            'death_date',
            'contacts',
        )
        exclude = []


class ContactMethodSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='contactmethod-detail',
    )

    class Meta:
        model = ContactMethod
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'detail',
            'email',
        )
        exclude = []


class CircleSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='circle-detail',
    )
    contacts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='contactmethod-detail',
        queryset=ContactMethod.objects.all(),
        required=False,
        allow_null=True,
    )
    invitations = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='invitation-detail',
    )

    class Meta:
        model = Circle
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'contacts',
            'reading_list',
            'invitations',
        )
        exclude = []


class InvitationSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='invitation-detail',
    )
    profile_to = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )
    circle = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='circle-detail',
        queryset=Circle.objects.all(),
    )

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
