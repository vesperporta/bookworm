"""Serializers to provide generic functionality."""
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from collections import OrderedDict

from authentication.models import Profile


class PreservedModelSerializeMixin:
    """Prevent deletion serializer mixin."""
    created_at = serializers.ReadOnlyField()
    modified_at = serializers.ReadOnlyField()
    deleted_at = serializers.ReadOnlyField()


class ProfileSerializeMixin:
    """Upon creation of objects assign profile from request object."""
    profile = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='profile-detail',
        queryset=Profile.objects.all(),
    )

    def create(self, validated_data):
        """Assign the current user to the validated_data object for creation.

        @:param validated_data: dict validated from request data.
        """
        validated_data.update({
            'profile': self.context['request'].user.profile,
        })
        return super().create(validated_data)


class ForeignFieldRepresentationSerializerMixin:

    def to_representation(self, instance):
        """Temporary override to enable the fetching of values defined
        by foreign key object representations.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            except AttributeError as error:
                if not self.Meta.foreign_fields_get:
                    raise error
                attribute = field.get_attribute(
                    getattr(
                        instance,
                        self.Meta.foreign_fields_get.get(field.field_name),
                    )
                )

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

