"""Books app views."""

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from authentication.models import (
    ContactMethod,
    Profile,
    Author,
)
from authentication.serializers import (
    ContactMethodSerializer,
    ProfileSerializer,
    AuthorSerializer,
    CircleSerializer,
    InvitationSerializer,
)
from authentication.models_circles import (
    Circle,
    Invitation,
)
from authentication.exceptions import (
    DuplicateInvitationValidationError,
    UnInvitationValidationError,
    InvitationValidationError,
    InvitationMissingError,
)


class InvitableViewSet:

    def _invitation_error_handle(self, error):
        """Handle errors supplied from invite actions.

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

    @detail_route(methods=['post'])
    def invite(self, request, pk, **kwargs):
        """Invite a profile to another object."""
        inviting_to = self.get_object()
        try:
            inviting_to.invite(
                Profile.objects.filter(user=request.user).first(),
                Profile.objects.filter(
                    id=request.POST.get('profile_to'),
                ).first(),
            )
        except (
            DuplicateInvitationValidationError,
            InvitationValidationError,
        ) as e:
            return self._invitation_error_handle(e)
        return Response(
            {
                'status': 'invited',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['post'])
    def invite_change(self, request, pk, **kwargs):
        """Change an invitation for a profile to a different type."""
        changing_for = self.get_object()
        try:
            changing_for.invite_change(
                Profile.objects.filter(user=request.user).first(),
                Profile.objects.filter(
                    id=request.POST.get('profile_to'),
                ).first(),
                request.POST.get('status'),
            )
        except (
            InvitationValidationError,
            InvitationMissingError,
        ) as e:
            return self._invitation_error_handle(e)
        return Response(
            {
                'status': 'changed',
                'ok': '🖖',
            }
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )


class ContactMethodViewSet(viewsets.ModelViewSet):
    queryset = ContactMethod.objects.all()
    serializer_class = ContactMethodSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail',)


class CircleViewSet(
        InvitableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
