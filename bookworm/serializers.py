"""Serializers to provide generic functionality."""
from rest_framework import serializers


class PreservedModelSerializeMixin:
    """Prevent deletion serializer mixin."""
    created_at = serializers.ReadOnlyField()
    modified_at = serializers.ReadOnlyField()
    deleted_at = serializers.ReadOnlyField()


class PublishableSerializeMixin:
    """Publishable base serializer for published endpoints."""
    pass
