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
    InvitationValidationError,
    InvitationMissingError,
    InvitationTokenNotExistError,
    InvitationAlreadyVerifiedError,
)
from authentication.tasks import task_send_message_invitable_action


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
                    id=request.data.get('profile_to'),
                ).first(),
            )
        except (
            DuplicateInvitationValidationError,
            InvitationValidationError,
        ) as e:
            return self._invitation_error_handle(e)
        task_send_message_invitable_action.delay('invite', inviting_to)
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
                    id=request.data.get('profile_to'),
                ).first(),
                request.POST.get('status'),
            )
        except (
            InvitationValidationError,
            InvitationMissingError,
        ) as e:
            return self._invitation_error_handle(e)
        task_send_message_invitable_action.delay('invite_change', changing_for)
        return Response(
            {
                'status': 'changed',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['post'])
    def invite_validate(self, request, pk, **kwargs):
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to=request.data.get('profile_to')
        )
        try:
            invite.token_verify(request.data.get('token'))
        except (
                InvitationTokenNotExistError,
                InvitationAlreadyVerifiedError,
        ) as e:
            return self._invitation_error_handle(e)
        task_send_message_invitable_action.delay(
            'invite_validate', changing_for)
        return Response(
            {
                'status': 'validated',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['post'])
    def invite_token_renew(self, request, pk, **kwargs):
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to=request.data.get('profile_to')
        )
        try:
            invite.token_recreate()
        except InvitationAlreadyVerifiedError as e:
            return self._invitation_error_handle(e)
        task_send_message_invitable_action.delay(
            'invite_token_renew', changing_for)
        return Response(
            {
                'status': 'validated',
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
