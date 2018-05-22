"""Books app serializers."""

from rest_framework import serializers


class PublishBookSerializer(serializers.ModelSerializer):
    """Book model serializer for publishing."""

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


class PublishBookProgressSerializer(serializers.ModelSerializer):
    """BookProgress model serializer for publishing."""
    book = PublishBookSerializer(many=False)

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


class PublishReadingListSerializer(serializers.ModelSerializer):
    """ReadingList publish serializer."""
    books = PublishBookSerializer(many=True)

    class Meta:
        model = 'books.models.ReadingList'
        read_only_fields = (
            'modified_at',
        )
        fields = read_only_fields + (
            'title',
            'copy',
            'books',
        )
        exclude = []


class PublishBookReviewSerializer(serializers.ModelSerializer):
    """BookReview publishable serializer."""
    book = PublishBookSerializer(many=False)
    progress = PublishBookProgressSerializer(many=False)

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'modified_at',
        )
        fields = read_only_fields + (
            'type',
            'copy',
            'rating',
            'book',
            'progress',
        )
        exclude = []
