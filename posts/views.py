"""Books app views."""

from rest_framework import (viewsets, filters)

from posts.models import (
    Emote,
    Post,
    Comment,
)
from meta_info.serializers import (
    EmoteSerializer,
    PostSerializer,
    CommentSerializer,
)


class EmoteViewSet(viewsets.ModelViewSet):
    queryset = Emote.objects.all()
    serializer_class = EmoteSerializer
    filter_backends = (filters.SearchFilter,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    search_fields = ('copy',)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    search_fields = ('copy',)
