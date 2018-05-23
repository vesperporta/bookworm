"""Posts app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from authentication.models import Profile
from posts.models import (
    Emote,
    Post,
    Comment,
)
from posts.serializers import (
    EmoteSerializer,
    PostSerializer,
    CommentSerializer,
)
from posts.exceptions import (
    InvalidEmoteModification,
    DuplicateEmoteValidationError,
    UnemoteValidationError,
)


class EmoteViewSet(viewsets.ModelViewSet):
    queryset = Emote.objects.all()
    serializer_class = EmoteSerializer
    filter_backends = (filters.SearchFilter,)


class EmotableViewSet:

    @detail_route(methods=['post'])
    def emoted(self, request, pk, **kwargs):
        emoting_on = self.get_object()
        try:
            emoting_on.emoted(
                request.POST.get('emote_type'),
                Profile.objects.filter(user=request.user).first(),
            )
        except DuplicateEmoteValidationError as e:
            return Response(
                {
                    'status': 'error',
                    'aggregate': emoting_on.emote_aggregation,
                    'error': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'status': 'emoted',
                'aggregate': emoting_on.emote_aggregation,
            }
        )

    @detail_route(methods=['post'])
    def demote(self, request, pk, **kwargs):
        emoting_on = self.get_object()
        try:
            emoting_on.demote(
                Profile.objects.filter(user=request.user).first(),
            )
        except UnemoteValidationError as e:
            return Response(
                {
                    'status': 'error',
                    'aggregate': emoting_on.emote_aggregation,
                    'error': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidEmoteModification as e:
            # emoting_on._emote_aggregation_from_db(self, )
            pass
        return Response(
            {
                'status': 'demoted',
                'aggregate': emoting_on.emote_aggregation,
            }
        )


class PostViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    search_fields = ('copy',)


class CommentViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    search_fields = ('copy',)
