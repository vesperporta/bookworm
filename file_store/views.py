"""FileStore app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework import decorators
from rest_framework.response import Response

from books.permissions import OwnerAndAdminPermission
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


class ImagableViewSet:

    def _image_error_handle(self, error):
        """Handle error responses from image.

        @param error: Exeption object.

        @return Response with 400 status code.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'error': error.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @decorators.detail_route(methods=['post'])
    @decorators.permission_classes((OwnerAndAdminPermission, ))
    def image_append(self, request, pk, **kwargs):
        """Add an Image to image list."""
        target = self.get_object()
        try:
            image = Image.objects.get(id=request.POST.get('image'))
        except Image.DoesNotExist as error:
            self._image_error_handle(error)
        target.image_append(image, request.POST.get('as_primary', False))
        return Response(
            {
                'status': 'appended',
                'ok': '🖖',
                'id': target.id,
                'images': target.images.values_list('id'),
            }
        )

    @decorators.detail_route(methods=['post'])
    @decorators.permission_classes((OwnerAndAdminPermission, ))
    def image_pop(self, request, pk, **kwargs):
        """Remove an image from object."""
        target = self.get_object()
        try:
            image = Image.objects.get(id=request.POST.get('image'))
        except Image.DoesNotExist as error:
            self._image_error_handle(error)
        target.image_pop(image)
        return Response(
            {
                'status': 'popped',
                'ok': '🖖',
                'id': target.id,
                'images': target.images.values_list('id'),
            }
        )


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', )
