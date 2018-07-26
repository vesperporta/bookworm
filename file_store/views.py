"""FileStore app views."""

from rest_framework import (status, viewsets, filters, )
from rest_framework import (decorators, permissions, )
from rest_framework.response import Response

from authentication.models import Profile
from books.permissions import OwnerAndAdminPermission
from file_store.models import (
    Image,
    Document,
)
from file_store.serializers import (
    ImageSerializer,
    DocumentSerializer,
)


class FilePermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions to allow specific status Profiles.

        Authenticated and elevated and above status Profiles.
        """
        authenticated = super().has_permission(request, view)
        if request.method in permissions.SAFE_METHODS:
            return True
        return authenticated

    def has_object_permission(self, request, view, obj):
        """Users may not accept their own answer.

        Admins are allowed to accept their own answers.
        """
        if request.method not in permissions.SAFE_METHODS:
            return (
                obj.profile.id == request.user.profile.id or
                request.user.profile.type >= Profile.TYPES.admin
            )
        return request.method in permissions.SAFE_METHODS


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', )
    permission_classes = (FilePermission, )


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
    permission_classes = (FilePermission, )
