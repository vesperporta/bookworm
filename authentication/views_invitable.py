"""Invitation mixin views."""

from rest_framework import (status, permissions)
from rest_framework.decorators import (detail_route, permission_classes)
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
from authentication.tasks import task_send_message_invitable_action


class InvitableInvitePermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Invite a Profile into this objects Profile list.

        Profiles with elevated and above Invites can invite others.
        Admins can invite anyone.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if not authenticated:
            return False
        if request.user.profile.type >= Profile.TYPES.admin:
            return True
        invite = obj.invites.filter(
            profile_to=request.user.profile,
        ).first()
        return invite and invite.status >= Invitation.STATUS.elevated


class InvitableInviteValidatePermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """A Profile can only validate their own token."""
        authenticated = super().has_object_permission(request, view, obj)
        if not authenticated:
            return False
        if request.user.profile.type >= Profile.TYPES.admin:
            return True
        invite = obj.invites.filter(
            profile_to=request.user.profile,
        )
        return invite and invite.status == Invitation.STATUS.invited


class InvitableInviteRenewTokenPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Invitations made can renew a token by the initiator.

        Profiles with elevated invitation status can renew an Invitation they
        issued to another Profile.
        Admins can renew any Invitation.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if not authenticated:
            return False
        if request.user.profile.type >= Profile.TYPES.admin:
            return True
        invite = obj.invites.filter(
            profile_to=request.user.profile,
        ).first()
        if not invite or invite.status < Invitation.STATUS.elevated:
            return False
        invite = obj.invites.filter(
            profile=request.user.profile,
            profile_to=request.data.get('profile_to'),
        ).first()
        return invite and invite.status == Invitation.STATUS.invited


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
    @permission_classes((InvitableInvitePermission, ))
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
    @permission_classes((InvitableInvitePermission, ))
    def invite_change(self, request, pk, **kwargs):
        """Change an invitation for a profile to a different type."""
        changing_for = self.get_object()
        try:
            invite = changing_for.invite_change(
                request.user.profile,
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
        task_send_message_invitable_action.delay(
            'invite_change', changing_for, invite)
        return Response(
            {
                'status': 'changed',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['post'])
    @permission_classes((InvitableInviteValidatePermission, ))
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
    @permission_classes((InvitableInviteRenewTokenPermission, ))
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
                error_status=status.HTTP_403_FORBIDDEN,
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
    @permission_classes((InvitableInvitePermission, ))
    def invites_withdrawn(self, request, pk, **kwargs):
        """List Invitations a Profile has withdrawn from."""
        inspecting = self.get_object()
        return Response(
            {
                'status': 'ok',
                'ok': '🖖',
                'withdrawn': list(inspecting.invites.filter(
                    status=Invitation.STATUSES.withdrawn,
                )),
            }
        )
