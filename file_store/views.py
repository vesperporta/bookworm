"""FileStore app views."""

from rest_framework import (viewsets, filters)

from file_store.models import (
    Image,
    Document,
)
from file_store.serializers import (
    ImageSerializer,
    DocumentSerializer,
)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', )
