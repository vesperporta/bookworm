"""Books app serializers."""

from django_common.auth_backends import User
from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from bookworm.exceptions import InvalidOperation
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
from authentication.models import (
    Profile,
    Author,
    ContactMethod,
)
from authentication.models_circles import (
    Circle,
    Invitation,
)
from authentication.models_token import Token


class ProfileSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='profile-detail',
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    pen_names = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='author-detail',
        read_only=True,
    )
    contacts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='contactmethod-detail',
        read_only=True,
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
        )
        exclude = []

    def create(self, validated_data):
        """Create a Profile object to allow a user to login.

        There is a requirement that a default Django User object is created
        first to allow the default allocation of information pertaining to
        the User object be transferred within a single task handler.

        @:param validated_data: dict validated from request data.

        @:returns Profile
        """
        email = validated_data.get('email')
        username = Token.objects.generate_sha256(email)
        with transaction.atomic():
            # Signals pre and post are contained within transaction.atomic.
            # User objects username field character limit is 150.
            created_user = User.objects.create_user(
                username=username[:150],
                email=email,
                password=validated_data.get('password'),
            )
        allowed_keys = [
            'name_title', 'name_first', 'name_family', 'name_middle',
            'name_display', 'birth_date', 'death_date',
        ]
        for key in allowed_keys:
            setattr(created_user.profile, key, validated_data.get(key))
        created_user.profile.save(update_fields=allowed_keys)
        return created_user.profile


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


class InvitationSerializer(
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
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )

    class Meta:
        model = Invitation
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'status',
            'profile',
            'profile_to',
        )
        fields = read_only_fields
        exclude = []

    def validate(self, data):
        """Validate for profile assignment to validated_data"""
        current_user = self.context['request'].user
        if current_user.id == data['profile_to']:
            raise InvalidOperation(self)
        return super().validate(data)


class CircleSerializer(
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
        read_only=True,
    )
    invites = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='invitation-detail',
        required=False,
    )

    class Meta:
        model = Circle
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'contacts',
            'reading_list',
            'invites',
        )
        exclude = []

    def create(self, validated_data):
        """Create a Circle object to group users.

        @:param validated_data: dict validated from request data.

        @:returns Circle
        """
        return Circle.objects.create_circle(
            self.context['request'].user.profile,
            **validated_data,
        )


class ProfileMeSerializer(
    MetaInfoAvailabledSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='profile-detail',
    )
    email = serializers.EmailField()
    pen_names = AuthorSerializer(
        many=True,
        read_only=True,
    )
    contacts = ContactMethodSerializer(
        many=True,
        read_only=True,
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
        )
        exclude = []
