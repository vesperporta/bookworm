"""Books app serializers."""

from rest_framework import serializers

from meta_info.models import (
    Tag,
    MetaInfo,
)


class TagSlugSerializer(serializers.ModelSerializer):
    """Short hand Tag serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='tag-detail',
    )

    class Meta:
        model = Tag
        read_only_fields = (
            'id',
            'slug',
        )
        fields = read_only_fields


class TagSerializer(serializers.ModelSerializer):
    """Generic Tag serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='tag-detail',
    )
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='tag-detail',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Tag
        read_only_fields = (
            'id',
            'slug',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'copy',
            'tags',
        )


class MetaInfoSerializer(serializers.HyperlinkedModelSerializer):
    """MetaInfo model serializer."""
    id = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='metainfo-detail',
    )
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='tag-detail',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = MetaInfo
        read_only_fields = (
            'id',
            'created_at',
            'modified_at',
            'deleted_at',
        )
        fields = read_only_fields + (
            'copy',
            'json',
            'tags',
        )
        exclude = ()


class MetaInfoAvailabledSerializerMixin:
    """Ensure the option for allowing the auto creation of meta_info.

    MetaInfo objects will only be created when all fields expected of that
    model are supplied as a JSON object.
    """

    meta_info = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='metainfo-detail',
        queryset=MetaInfo.objects.all(),
        required=False,
        allow_null=True,
    )

    def create(self, validated_data):
        """Create for meta_info to validated_data"""
        if 'meta_info' in validated_data and \
                not type(validated_data['meta_info']) is str:
            meta_info = MetaInfo.objects.create(**validated_data['meta_info'])
            validated_data.update({
                'meta_info': meta_info,
            })
        return super().create(validated_data)
