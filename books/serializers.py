"""Books app serializers."""

from rest_framework import serializers

from bookworm.exceptions import DataMissingValidationError
from bookworm.serializers import ProfileRefferedSerializerMixin
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


class BooklessBookProgressSerializer(
        ProfileRefferedSerializerMixin,
        serializers.ModelSerializer,
):
    """BookProgress model serializer."""

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'start',
            'end',
        )


class BooklessBookReviewSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    """BookReview serializer."""
    progress = BooklessBookProgressSerializer(many=False)

    class Meta:
        model = BookReview
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
            'progress',
        )
        exclude = []


class BookSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    """Book model serializer."""
    reviews = BooklessBookReviewSerializer(many=True)

    class Meta:
        model = Book
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'description',
            'reviews',
            'meta_info',
        )
        exclude = []


class BookProgressSerializer(
        ProfileRefferedSerializerMixin,
        serializers.ModelSerializer,
):
    """BookProgress model serializer."""
    book = BookSerializer(many=False)

    class Meta:
        model = BookProgress
        exclude = []
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'start',
            'end',
            'book',
        )


class BookChapterSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    """BookChapter serializer."""
    book = BookSerializer(many=False)
    progress = BookProgressSerializer(many=False)

    class Meta:
        model = BookChapter
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
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
        serializers.ModelSerializer,
):
    """ReadingList serializer."""
    books = BookSerializer(many=True)

    class Meta:
        model = ReadingList
        read_only_fields = (
            'profile',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'books',
        )
        exclude = []


class BookReviewSerializer(
        ProfileRefferedSerializerMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.ModelSerializer,
):
    """BookReview serializer."""
    book = BookSerializer(many=False)
    progress = BookProgressSerializer(many=False)

    class Meta:
        model = BookReview
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
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
):
    """Thrill model serializer."""
    book = BookSerializer(many=False)
    reading_list = ReadingListSerializer(many=False)

    def validate(self, data):
        """Validate for XOR assignment between book and reading_list."""
        book_id = data['book']
        reading_list_id = data['reading_list']
        if (not book_id and not reading_list_id) or \
                (book_id and reading_list_id):
            raise DataMissingValidationError(data, 'book', 'reading_list')
        return super().validate(data)

    class Meta:
        model = Thrill
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'book',
            'reading_list',
        )
        exclude = []


class ConfirmReadQuestionSerializer(
        ProfileRefferedSerializerMixin,
):
    """ConfirmReadQuestion model serializer."""
    book = BookSerializer(many=False)
    chapter = BookChapterSerializer(many=False)

    class Meta:
        model = ConfirmReadQuestion
        read_only_fields = (
            'created_at',
            'modified_at',
            'deleted_at',
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
):
    """ConfirmRead model serializer."""
    book = BookSerializer(many=False)

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
