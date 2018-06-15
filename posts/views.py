"""Posts app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from authentication.models import Profile
from posts.models import (
    Emote,
    Post,
)
from posts.serializers import (
    EmoteSerializer,
    PostSerializer,
)
from posts.exceptions import (
    InvalidEmoteModification,
    DuplicateEmoteValidationError,
    UnemoteValidationError,
)
from file_store.views import ImagableViewSet


class EmoteViewSet(viewsets.ModelViewSet):
    queryset = Emote.objects.all()
    serializer_class = EmoteSerializer


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
    def emoted(self, request, pk, **kwargs):
        """Add an Emote object to an object."""
        emoting_on = self.get_object()
        try:
            emoting_on.emoted(
                request.POST.get('emote_type'),
                Profile.objects.filter(user=request.user).first(),
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
                'aggregate': emoting_on.emote_aggregation,
            }
        )

    @detail_route(methods=['post'])
    def demote(self, request, pk, **kwargs):
        """Remove an Emote from an object."""
        emoting_on = self.get_object()
        try:
            emoting_on.demote(
                Profile.objects.filter(user=request.user).first(),
            )
        except (
            UnemoteValidationError,
            InvalidEmoteModification,
        ) as error:
            return self._emote_error_handle(emoting_on, error)
        return Response(
            {
                'status': 'demoted',
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
