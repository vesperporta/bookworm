"""Mixin views."""

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from bookworm.exceptions import (
    PublishableValidationError,
    PublishableObjectNotDefined,
)


class PublishableViewSetMixin:

    def _publishing_error_handle(self, error):
        """Handle errors supplied from publishing actions.

        @param error: Exception object.

        @return Response with 404 status code.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'error': error.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @detail_route(methods=['post'])
    def publish(self, request, pk, **kwargs):
        """Publish this object."""
        publishing = self.get_object()
        try:
            publishing.publish(
                request.data.get('granted'),
                request.data.get('block'),
            )
        except (
                PublishableValidationError,
                PublishableObjectNotDefined,
        ) as error:
            return self._publishing_error_handle(error)
        return Response(
            {
                'status': 'published',
                'ok': '🖖',
                'detail': publishing.published_meta.json.output,
            },
        )

    @detail_route(methods=['post'])
    def unpublish(self, request, pk, **kwargs):
        """Unpublish this object."""
        unpublishing = self.get_object()
        unpublish_method = 'unpublish'
        if bool(request.data.get('purge')):
            unpublish_method = 'unpublish_purge'
        try:
            getattr(unpublishing, unpublish_method)()
        except PublishableValidationError as error:
            return self._publishing_error_handle(error)
        return Response(
            {
                'status': 'unpublished',
                'ok': '🖖',
            },
        )
