"""Books app serializers."""

from rest_framework import serializers

from bookworm.serializers import ProfileRefferedSerializerMixin
from meta_info.serializers import MetaSerializer


class BookSerializer(MetaSerializer, ProfileRefferedSerializerMixin):
    class Meta:
        model = 'books.models.Book'
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'description',
            'reviews',
            'meta',
        )
        exclude = []


class PublishBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'books.models.Book'
        read_only_fields = (
            'id',
            'modified_at',
        )
        fields = read_only_fields + (
            'title',
            'description',
        )
        exclude = []


class BookProgressSerializer(
        serializers.ModelSerializer, ProfileRefferedSerializerMixin):
    book = BookSerializer()

    class Meta:
        model = 'books.models.BookProgress'
        exclude = []
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'progress',
            'book',
        )


class PublishBookProgressSerializer(serializers.ModelSerializer):
    book = PublishBookSerializer()

    class Meta:
        model = 'books.models.BookProgress'
        exclude = []
        read_only_fields = (
            'modified_at',
        )
        fields = read_only_fields + (
            'percent',
            'page',
            'progress',
            'book',
        )


class ReadingListSerializer(MetaSerializer, ProfileRefferedSerializerMixin):
    books = BookSerializer(many=True)

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'copy',
            'books',
        )
        exclude = []


class PublishReadingListSerializer(serializers.ModelSerializer):
    books = PublishBookSerializer(many=True)

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'modified_at',
        )
        fields = read_only_fields + (
            'title',
            'copy',
            'books',
        )
        exclude = []


class BookReviewSerializer(MetaSerializer, ProfileRefferedSerializerMixin):
    book = BookSerializer()
    progress = BookProgressSerializer()

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'book',
            'progress',
        )
        exclude = []


class PublishBookReviewSerializer(serializers.ModelSerializer):
    book = PublishBookSerializer()
    progress = PublishBookProgressSerializer()

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'modified_at',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'book',
            'progress',
        )
        exclude = []
