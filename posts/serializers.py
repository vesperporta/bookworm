"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import PreservedModelSerializeMixin
from meta_info.serializers import MetaInfoAvailabledSerializerMixin

from authentication.models import Profile
from file_store.models import Image
from posts.models import (
    Emote,
    Post,
)


class EmoteSerializer(
        PreservedModelSerializeMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Generic Emote serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='emote-detail',
    )
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )

    class Meta:
        model = Emote
        read_only_fields = (
            'id',
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'type',
        )


class SmallEmoteSerializer(serializers.HyperlinkedModelSerializer):
    """Small Emote serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='emote-detail',
    )
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Emote
        read_only_fields = (
            'id',
            'created_at',
            'type',
        )
        fields = ()


class EmotableSerializerMixin:
    """Generic Emotable serializer."""

    emotes = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='emote-detail',
        queryset=Emote.objects.all(),
    )
    emote_aggregate = serializers.ListField(
        child=serializers.IntegerField(
            min_value=0,
            max_value=None,
        ),
        min_length=len(Emote.EMOTES),
        max_length=len(Emote.EMOTES),
    )


class ThinPostSerializer(serializers.HyperlinkedModelSerializer):
    """Post model (but a thin) serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='post-detail',
    )
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        read_only_fields = (
            'id',
            'copy',
            'children_count',
        )
        fields = read_only_fields
        exclude = ()

    def get_children_count(self, obj):
        return obj.children.all().count()


class PostSerializer(
        EmotableSerializerMixin,
        PreservedModelSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Post model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='post-detail',
    )
    parent = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='post-detail',
        queryset=Post.objects.all(),
        required=False,
        allow_null=True,
    )
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )
    images = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )
    cover_image = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )
    children = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail',
    )
    children_count = serializers.SerializerMethodField()
    children_preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        read_only_fields = (
            'id',
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'emotes',
            'emote_aggregate',
            'children',
            'children_count',
            'children_preview',
            'images',
        )
        fields = read_only_fields + (
            'copy',
            'parent',
            'cover_image',
        )
        exclude = ()

    def get_children_count(self, obj):
        return obj.children.all().count()

    def get_children_preview(self, obj):
        data = []
        for child in obj.children.all().order_by('-created_at')[:3]:
            serializer = ThinPostSerializer(child, context=self.context)
            data.append(serializer.data)
        return data
