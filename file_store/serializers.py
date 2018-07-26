"""FileStore app serializers."""

from rest_framework import serializers

from bookworm.serializers import (
    PreservedModelSerializeMixin,
    ProfileSerializeMixin,
)
from meta_info.serializers import MetaInfoAvailabledSerializerMixin

from file_store.models import (
    Image,
    Document,
)


class ImageSerializer(
    ProfileSerializeMixin,
    PreservedModelSerializeMixin,
    MetaInfoAvailabledSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    """Image serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='image-detail',
    )
    original = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Image
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
            'profile',
            'original',
            'meta_info',
        )
        fields = read_only_fields + (
            'title',
            'description',
            'mime',
            'source_url',
        )
        exclude = []


class DocumentSerializer(
        PreservedModelSerializeMixin,
        MetaInfoAvailabledSerializerMixin,
        serializers.HyperlinkedModelSerializer,
):
    """Document serializer."""

    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='document-detail',
    )
    cover = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='image-detail',
        queryset=Image.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Document
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'title',
            'description',
            'extension',
            'mime',
            'source_url',
            'file',
            'cover',
        )
        exclude = []
