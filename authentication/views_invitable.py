"""Invitation mixin views."""

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from authentication.models import Profile
from authentication.models_circles import Invitation
from authentication.exceptions import (
    DuplicateInvitationValidationError,
    InvitationValidationError,
    InvitationMissingError,
    InvitationTokenNotExistError,
    InvitationAlreadyVerifiedError,
)
from authentication.serializers import InvitationSerializer
from authentication.tasks import task_send_message_invitable_action


class InvitableViewSetMixin:

    def _invitation_error_handle(self, error, error_status=None):
        """Handle errors supplied from invite actions.

        @param error: Exception object.

        @return Response with 404 status code.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'error': error.get('detail'),
            },
            status=error_status or status.HTTP_400_BAD_REQUEST,
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
        """Validate a token of an Invitation and accept Invitation."""
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to=request.data.get('profile_to'),
            status=Invitation.STATUSES.invited,
        )
        try:
            invite.token_verify(request.data.get('token'))
        except InvitationTokenNotExistError as error:
            return self._invitation_error_handle(
                error, error_status=status.HTTP_404_NOT_FOUND, )
        except InvitationAlreadyVerifiedError as error:
            return self._invitation_error_handle(error)
        invite.status = Invitation.STATUSES.accepted
        invite.save()
        task_send_message_invitable_action.delay(
            'invite_validate', changing_for, invite)
        return Response(
            {
                'status': 'validated',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['post'])
    def invite_token_renew(self, request, pk, **kwargs):
        """Renew an invitations' token for acceptance.

        Creator of the Invitation may renew the token.
        """
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to__id=request.data.get('profile_to'),
            profile__id=request.user.profile.id,
            status=Invitation.STATUSES.invited,
        )
        if not invite:
            return self._invitation_error_handle(
                {'detail': _('Not Found'), },
                error_status=status.HTTP_404_NOT_FOUND,
            )
        try:
            invite.token_recreate()
        except InvitationAlreadyVerifiedError as e:
            return self._invitation_error_handle(e)
        task_send_message_invitable_action.delay(
            'invite_token_renew', changing_for)
        return Response(
            {
                'status': 'renewed',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['get'])
    def invites_withdrawn(self, request, pk, **kwargs):
        """List Invitations a Profile has withdrawn from."""
        inspecting = self.get_object()
        if not inspecting.invites.filter(
                profile_to__id=request.user.profile.id,
                status=Invitation.STATUSES.elevated,
        ).first():
            return self._invitation_error_handle(
                {'detail': _('unauthorized'), },
                error_status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {
                'status': 'ok',
                'ok': '🖖',
                'withdrawn': list(inspecting.invites.filter(
                    status=Invitation.STATUSES.withdrawn,
                )),
            }
        )
