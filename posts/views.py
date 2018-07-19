"""Posts app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import (detail_route, permission_classes, )
from rest_framework import permissions
from rest_framework.response import Response

from books.permissions import AnyReadOwnerCreateEditPermission
from posts.models import (
    Emote,
    Post,
)
from posts.serializers import (
    PostSerializer,
    EmoteSerializer,
    SmallEmoteSerializer,
)
from posts.exceptions import (
    InvalidEmoteModification,
    DuplicateEmoteValidationError,
    UnemoteValidationError,
    EmoteFieldMissingValidationError)
from file_store.views import ImagableViewSet


class EmoteViewSet(viewsets.ModelViewSet):
    queryset = Emote.objects.all()
    serializer_class = EmoteSerializer
    permission_classes = (AnyReadOwnerCreateEditPermission, )


class EmotableViewSet:

    def _emote_error_handle(self, emoting_on, error):
        """Handle error responses from emotes.

        @param emoting_on: Emotable object.
        @param error: Exeption object.

        @return Response with 400 status code.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'aggregate': emoting_on.emote_aggregation,
                'error': error.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @detail_route(methods=['post'])
    @permission_classes((permissions.IsAuthenticated, ))
    def emoted(self, request, pk, **kwargs):
        """Add an Emote object to an object."""
        emoting_on = self.get_object()
        if not request.data.get('emote_type'):
            return self._emote_error_handle(
                emoting_on,
                EmoteFieldMissingValidationError('emote_type'),
            )
        try:
            emote = emoting_on.emoted(
                request.data.get('emote_type'),
                request.user.profile,
            )
        except (
            DuplicateEmoteValidationError,
            InvalidEmoteModification,
        ) as error:
            return self._emote_error_handle(emoting_on, error)
        return Response(
            {
                'status': 'emoted',
                'ok': '🖖',
                'emote': SmallEmoteSerializer(
                    emote,
                    context={'request': request}
                ).data,
                'aggregate': emoting_on.emote_aggregation,
            }
        )

    @detail_route(methods=['post'])
    @permission_classes((permissions.IsAuthenticated, ))
    def un_emote(self, request, pk, **kwargs):
        """Remove an Emote from an object."""
        emoting_on = self.get_object()
        try:
            emoting_on.un_emote(request.user.profile)
        except (
            UnemoteValidationError,
            InvalidEmoteModification,
        ) as error:
            return self._emote_error_handle(emoting_on, error)
        return Response(
            {
                'status': 'un-emoted',
                'ok': '🖖',
                'aggregate': emoting_on.emote_aggregation,
            }
        )


class PostViewSet(
        EmotableViewSet,
        ImagableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy', 'parent__id', )
    permission_classes = (AnyReadOwnerCreateEditPermission, )
