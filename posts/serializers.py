"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import (
    ProfileRefferedSerializerMixin,
    PreservedModelSerializeMixin,
)
from meta_info.serializers import MetaInfoAvailabledSerializerMixin

from posts.models import (
    Emote,
    Post,
    Comment,
)


class EmoteSerializer(
        ProfileRefferedSerializerMixin,
        PreservedModelSerializeMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Generic Emote serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='emote-detail',
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


class PostSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
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
    comments = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='comment-detail',
        queryset=Comment.objects.all(),
    )
    comments_count = serializers.SerializerMethodField()
    comments_preview = serializers.SerializerMethodField()

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
            'comments',
            'comments_count',
            'comments_preview',
        )
        fields = read_only_fields + (
            'copy',
        )
        exclude = ()

    def get_comments_count(self, obj):
        return obj.comments.all().count()

    def get_comments_preview(self, obj):
        return obj.comments.all().order_by('-created_at')[:3]


class CommentSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        PreservedModelSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Comment model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='comment-detail',
    )
    post = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='post-detail',
        queryset=Post.objects.all(),
    )

    class Meta:
        model = Comment
        read_only_fields = (
            'id',
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'copy',
            'post',
        )
        exclude = ()
