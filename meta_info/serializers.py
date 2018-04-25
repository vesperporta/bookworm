"""Books app serializers."""

from rest_framework import serializers

from meta_info.models import (
    Tag,
    MetaInfo,
)


class TagSlugSerializer(serializers.ModelSerializer):
    """Short hand Tag serializer."""

    class Meta:
        model = Tag
        read_only_fields = (
            'id',
            'slug',
        )
        fields = read_only_fields


class TagSerializer(serializers.ModelSerializer):
    """Generic Tag serializer."""

    tags = TagSlugSerializer(many=True)

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


class MetaInfoSerializer(serializers.ModelSerializer):
    """MetaInfo model serializer."""

    tags = TagSerializer(many=True)

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

    meta_info = MetaInfoSerializer(many=False)

    def validate(self, data):
        """Validate for meta_info to validated_data"""
        if 'meta_info' in data and not type(data['meta_info']) is str:
            meta_info = MetaInfo.objects.create(**data['meta_info'])
            data['meta_info'] = meta_info.id
        return super().validate(data)
