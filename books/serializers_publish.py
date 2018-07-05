"""Books app serializers."""

from rest_framework import serializers


class BookReviewPublishSerializer(serializers.ModelSerializer):
    """BookReview publishable serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='bookreview-detail',
    )

    class Meta:
        model = 'books.models.BookReview'
        read_only_fields = (
            'id',
            'created_at',
            'profile',
            'type',
            'copy',
            'rating',
        )
        fields = read_only_fields
        exclude = []
