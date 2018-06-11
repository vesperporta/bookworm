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
)


class InvitableViewSet:

    @detail_route(methods=['post'])
    def invite(self, request, pk, **kwargs):
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
            return Response(
                {
                    'status': 'error',
                    'error': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'status': 'invited',
            }
        )

    @detail_route(methods=['post'])
    def invite_change(self, request, pk, **kwargs):
        changing_for = self.get_object()
        try:
            changing_for.invite_change(
                Profile.objects.filter(user=request.user).first(),
                Profile.objects.filter(
                    id=request.POST.get('profile_to'),
                ).first(),
                request.POST.get('status'),
            )
        except InvitationValidationError as e:
            return Response(
                {
                    'status': 'error',
                    'error': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'status': 'changed',
            }
        )

    @detail_route(methods=['post'])
    def uninvite(self, request, pk, **kwargs):
        uninviting_from = self.get_object()
        try:
            uninviting_from.uninvite(
                Profile.objects.filter(
                    id=request.POST.get('profile_to'),
                ).first(),
            )
        except (
            UnInvitationValidationError,
            InvitationValidationError,
        ) as e:
            return Response(
                {
                    'status': 'error',
                    'error': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'status': 'uninvited',
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
