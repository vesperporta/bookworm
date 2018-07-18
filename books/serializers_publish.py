"""Books app serializers."""

from django.utils.timezone import now

from rest_framework import serializers

from authentication.models import Profile
from books.models import (
    Book,
    BookProgress,
    BookChapter,
    BookReview,
)
from books.models_read import (
    ConfirmReadQuestion,
    ConfirmReadAnswer,
    Read,
)
from file_store.models import Image


class ShortBookPublishSerializer(serializers.ModelSerializer):
    """Short Book serializer for published objects."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    cover_image = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Book
        read_only_fields = (
            'id',
            'title',
            'author',
            'description',
            'cover_image',
        )
        fields = read_only_fields
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'reviews',
            'meta_info',
            'isbn',
            'ean',
            'documents',
            'images',
            'profile',
            'emotes',
            'emote_aggregate',
        ]


class ShortBookProgressPublishSerializer(
    serializers.HyperlinkedModelSerializer,
):
    """BookProgress serializer for publishing."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookprogress-detail',
    )

    class Meta:
        model = BookProgress
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'book',
            'document',
        ]
        read_only_fields = (
            'id',
            'percent',
            'page',
            'start',
            'end',
        )
        fields = read_only_fields


class ShortBookChapterPublishSerializer(serializers.HyperlinkedModelSerializer):
    """BookChapter serializer for publishing."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookchapter-detail',
    )
    progress = ShortBookProgressPublishSerializer()

    class Meta:
        model = BookChapter
        read_only_fields = (
            'id',
            'title',
            'progress',
        )
        fields = read_only_fields
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'book',
        ]


class BookReviewPublishSerializer(serializers.ModelSerializer):
    """BookReview publishable serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )
    created_at = serializers.SerializerMethodField()
    book = ShortBookPublishSerializer()
    progress = ShortBookProgressPublishSerializer()
    inferred_progress = ShortBookProgressPublishSerializer()

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'created_at',
            'profile',
            'type',
            'copy',
            'rating',
            'book',
            'progress',
            'inferred_progress',
        )
        fields = read_only_fields
        exclude = []

    def get_created_at(self):
        return now(USE_TZ=True).isoformat()


class ShortConfirmReadQuestionPublishSerializer(
    serializers.HyperlinkedModelSerializer
):
    """ConfirmReadQuestion serializer for publishing (short)."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadquestion-detail',
    )

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'id',
            'difficulty',
            'copy',
        )
        fields = read_only_fields
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'emotes',
            'emote_aggregate',
            'book',
            'chapter',
        ]


class ConfirmReadQuestionPublishSerializer(
    serializers.HyperlinkedModelSerializer
):
    """ConfirmReadQuestion serializer for publishing."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadquestion-detail',
    )
    book = ShortBookPublishSerializer()
    chapter = ShortBookChapterPublishSerializer()

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'id',
            'difficulty',
            'book',
            'chapter',
            'copy',
        )
        fields = read_only_fields
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'emotes',
            'emote_aggregate',
        ]


class ConfirmReadAnswerPublishSerializer(
    serializers.HyperlinkedModelSerializer
):
    """ConfirmReadAnswer model serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadanswer-detail',
    )
    accepted_by = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )
    question = ShortConfirmReadQuestionPublishSerializer()

    class Meta:
        model = ConfirmReadAnswer
        read_only_fields = (
            'id',
            'accepted_at',
            'accepted_by',
            'question',
            'is_true',
            'copy',
        )
        fields = read_only_fields
        exclude = [
            'is_answer',
            'created_at',
            'modified_at',
            'deleted_at',
        ]


class ReadPublishSerializer(serializers.HyperlinkedModelSerializer):
    """ConfirmRead model serializer for publishing."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='read-detail',
    )
    book = ShortBookPublishSerializer()
    answered_correctly = serializers.BooleanField()
    answer = ConfirmReadAnswerPublishSerializer()

    class Meta:
        model = Read
        read_only_fields = (
            'id',
            'book',
            'answered_correctly',
            'answer',
        )
        fields = read_only_fields
        exclude = [
            'created_at',
            'modified_at',
            'deleted_at',
            'emotes',
            'emote_aggregate',
        ]
