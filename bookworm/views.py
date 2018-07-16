"""Mixin views."""

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from bookworm.exceptions import (
    PublishableValidationError,
    PublishableObjectNotDefined,
    PublishedUnauthorisedValidation,
    NoPublishedDataError,
)


class PublishableViewSetMixin:

    def _publishing_error_handle(self, error, status_response=None):
        """Handle errors supplied from publishing actions.

        @:param error: Exception object.
        @:param status_response: int

        @return Response with 404 status code, unless defined.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'error': error.detail,
            },
            status=status_response or status.HTTP_400_BAD_REQUEST,
        )

    @detail_route(methods=['get'])
    def published_content(self, request, pk, **kwargs):
        """Respond with the published content for this object."""
        published = self.get_object()
        try:
            content = published.published_content(request.user.profile)
        except PublishedUnauthorisedValidation as error:
            return self._publishing_error_handle(
                error,
                status.HTTP_401_UNAUTHORIZED,
            )
        except NoPublishedDataError as error:
            return self._publishing_error_handle(error)
        return Response(content)

    @detail_route(methods=['post'])
    def publish(self, request, pk, **kwargs):
        """Publish this object."""
        # TODO: Authentication for publishing.
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
        # TODO: Authentication for unpublishing.
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
