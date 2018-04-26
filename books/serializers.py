"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import (
    ProfileRefferedSerializerMixin,
    PreservedModelSerializeMixin,
)
from meta_info.serializers import MetaInfoAvailabledSerializerMixin

from books.models import (
    Book,
    BookProgress,
    BookChapter,
    ReadingList,
    BookReview,
)
from books.models_read import (
    Thrill,
    ConfirmReadQuestion,
    ConfirmReadAnswer,
    Read,
)


class BookReviewShortSerializer(
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
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
        )
        exclude = []


class BookSerializer(
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
        )
        fields = read_only_fields + (
            'title',
            'description',
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
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'books',
        )
        exclude = []


class BookReviewSerializer(
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
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
            'book',
            'progress',
        )
        exclude = []


class ThrillSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Thrill model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='thrill-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    reading_list = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )

    class Meta:
        model = Thrill
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'book',
            'reading_list',
        )
        exclude = []


class BookThrillSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Thrill model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='thrill-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )
    reading_list = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='readinglist-detail',
    )

    class Meta:
        model = Thrill
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'book',
            'reading_list',
        )
        exclude = []

    def create(self, validated_data):
        validated_data['reading_list'] = None
        return super().create(validated_data)


class ReadingListThrillSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Thrill model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='thrill-detail',
    )
    book = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='book-detail',
    )
    reading_list = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='readinglist-detail',
        queryset=ReadingList.objects.all(),
    )

    class Meta:
        model = Thrill
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'book',
            'reading_list',
        )
        exclude = []


class ConfirmReadQuestionSerializer(
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
    )

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
        )
        fields = read_only_fields + (
            'difficulty',
            'book',
            'chapter',
            'question',
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
        )
        fields = read_only_fields + (
            'question',
            'answer',
            'copy',
        )
        exclude = []


class ReadSerializer(
        ProfileRefferedSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """ConfirmRead model serializer."""
    book = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='book-detail',
        queryset=Book.objects.all(),
    )

    class Meta:
        model = Read
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'book',
            'question',
            'answer',
        )
        exclude = []
