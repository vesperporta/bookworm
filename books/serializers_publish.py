"""Books app serializers."""

from rest_framework import serializers

from books.models import BookReview


class BookReviewPublishSerializer(serializers.ModelSerializer):
    """BookReview publishable serializer."""

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
            'profile',
            'type',
            'copy',
            'rating',
            'book',
            'progress',
        )
        fields = read_only_fields
        exclude = []
