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
        """Documents may only be changed by an administrator otherwise read."""
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
        """Add an Image to image list.

        Request param of `images` is acceptable for a list of images to be
        added to the target object at one time otherwise the request param of
        `image` is always attempted when the former is not defined.

        Request param `as_primary` is used as either a string identifier for
        the image being added from a list or is a boolean when a single image
        is being added to the target.
        """
        target = self.get_object()
        images_list = request.POST.get('images')
        as_primary = request.POST.get('as_primary', False)
        if images_list:
            images = Image.objects.filter(id__in=images_list)
            for image in images:
                target.image_append(
                    image,
                    True if (
                        type(as_primary) is str and
                        as_primary == image.id
                    ) else False
                )
        else:
            try:
                image = Image.objects.get(id=request.POST.get('image'))
                target.image_append(
                    image,
                    bool(as_primary),
                )
            except Image.DoesNotExist as error:
                self._image_error_handle(error)
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
        """Remove an image from object.

        Request params of `images` is operated on as an array of image ids
        where all known images are removed from the target, otherwise a single
        `image` parameter is used to remove a single image.

        When a cover_image is removed from the list of images that image is
        removed from the cover image and replaced with the first available
        image in the available list or None.
        """
        target = self.get_object()
        images_list = request.POST.get('images')
        if images_list:
            images = Image.objects.filter(id__in=images_list)
            for image in images:
                target.image_pop(image)
        else:
            try:
                image = Image.objects.get(id=request.POST.get('image'))
                target.image_pop(image)
            except Image.DoesNotExist as error:
                self._image_error_handle(error)
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
