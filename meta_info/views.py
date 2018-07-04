"""Books app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from meta_info.models import (
    Tag,
    MetaInfo,
)
from meta_info.serializers import (
    TagSerializer,
    MetaInfoSerializer,
)
from meta_info.exceptions import (
    LocalisationUnknownLocaleException,
    LocalisationCodeRequiredValidation,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy',)


class MetaViewSet(viewsets.ModelViewSet):
    queryset = MetaInfo.objects.all()
    serializer_class = MetaInfoSerializer


class LocalisableViewSetMixin:

    def _localisation_error_handle(self, error):
        """Handle errors supplied from localisation actions.

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

    @detail_route(methods=['get'])
    def localised(self, request, pk, **kwargs):
        """Localise object to specified '{language}-{location}'."""
        localising_for = self.get_object()
        query_locale_code = request.query_params.get('locale')
        if not query_locale_code:
            return self._localisation_error_handle(
                LocalisationCodeRequiredValidation('locale')
            )
        try:
            localised = localising_for.locale_as(query_locale_code)
        except LocalisationUnknownLocaleException as error:
            return self._localisation_error_handle(error)
        return Response(
            {
                'status': 'localised',
                'ok': '🖖',
                'detail': localised,
            },
        )
