"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import (
    ProfileRefferedSerializerMixin,
    PreservedModelSerializeMixin,
)
from meta_info.serializers import MetaInfoAvailabledSerializerMixin
from posts.serializers import EmotableSerializerMixin

from books.models import (
    Book,
    BookProgress,
    BookChapter,
    ReadingList,
    BookReview,
)
from books.models_read import (
    ConfirmReadQuestion,
    ConfirmReadAnswer,
    Read,
)


class BookReviewShortSerializer(
        EmotableSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookReview serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
        )
        exclude = []


class BookSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        PreservedModelSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Book model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    reviews = BookReviewShortSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Book
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'reviews',
            'meta_info',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'title',
            'author',
            'description',
            'isbn',
            'ean',
        )
        exclude = []


class BookProgressSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookProgress model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookprogress-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'start',
            'end',
            'book',
        )


class BookChapterSerializer(
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookChapter serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookchapter-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    progress = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='bookprogress-detail',
        queryset=BookProgress.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BookChapter
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'progress',
            'book',
        )
        exclude = []


class ReadingListSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ReadingList serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )
    books = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )

    class Meta:
        model = ReadingList
        read_only_fields = (
            'id',
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
            'emotes',
            'emote_aggregate',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'books',
        )
        exclude = []


class BookReviewSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """BookReview serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    progress = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='bookprogress-detail',
        queryset=BookProgress.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = BookReview
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'meta_info',
            'profile',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
            'book',
            'progress',
        )
        exclude = []


class ConfirmReadQuestionSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ConfirmReadQuestion model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='confirmreadquestion-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    chapter = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='bookchapter-detail',
        queryset=BookChapter.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'difficulty',
            'book',
            'chapter',
            'copy',
        )
        exclude = []


class ConfirmReadAnswerSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ConfirmReadAnswer model serializer."""

    class Meta:
        model = ConfirmReadAnswer
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
            'accepted_at',
            'accepted_by',
        )
        fields = read_only_fields + (
            'question',
            'is_true',
            'is_answer',
            'copy',
        )
        exclude = []


class ReadSerializer(
        EmotableSerializerMixin,
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ConfirmRead model serializer."""
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    answered_correctly = serializers.BooleanField(
        read_only=True,
    )

    class Meta:
        model = Read
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
            'answered_correctly',
            'emotes',
            'emote_aggregate',
        )
        fields = read_only_fields + (
            'book',
            'answer',
        )
        exclude = []
