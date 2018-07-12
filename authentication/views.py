"""Books app views."""

from rest_framework import (status, viewsets, filters, permissions)
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
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to=request.data.get('profile_to')
        )
        try:
            invite.token_verify(request.data.get('token'))
        except InvitationTokenNotExistError as error:
            return self._invitation_error_handle(
                error, error_status=status.HTTP_404_NOT_FOUND, )
        except InvitationAlreadyVerifiedError as error:
            return self._invitation_error_handle(error)
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
        """Renew an invitations' token for acceptance.

        Creator of the Invitation may renew the token.
        """
        changing_for = self.get_object()
        invite = changing_for.invites.filter(
            profile_to__id=request.data.get('profile_to'),
            profile__id=request.user.profile.id,
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
                'status': 'validated',
                'ok': '🖖',
            }
        )

    @detail_route(methods=['get'])
    def invites_withdrawn(self, request, pk, **kwargs):
        """Invite a profile to another object."""
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


class ProfilePermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions for the Profile model.

        Always allow create when not authenticated.
        To view or manage your profile: be authenticated.
        Admins are allowed to see all.
        """
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        if view.action in ['create']:
            if authenticated:
                return False
            return True
        return authenticated

    def has_object_permission(self, request, view, obj):
        """Users may only see and manage their own Profile.

        Admins are allowed to manage other peoples profiles.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated and obj.id == request.user.profile.id


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermission, )
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )

    def get_queryset(self):
        """User may only see their own Profile object.

        Admins can view all Profiles.
        """
        queryset = super().get_queryset()
        if (
                self.action in ['list']
                and self.request.user.profile.type < Profile.TYPES.admin
        ):
            return queryset.filter(id=self.request.user.profile.id)
        return queryset


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
    search_fields = (
        'detail',
    )


class AuthenticatedOrAdminPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions required are an authenticated user or admin."""
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated


class CirclePermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Permissions to manage access to a Circle model.

        Allow all create.
        Users invited and accepted to a circle can retrieve.
        Users invited and set as admin can [update, partial_update, destroy]
        Admins can do everything.
        """
        is_admin = request.user.profile.type >= Profile.TYPES.admin
        accepted_invite = obj.invites.filter(
            profile_to__id=request.user.profile.id,
            status__gt=Invitation.STATUSES.invited,
        ).first()
        if not accepted_invite:
            return request.method in ['create']
        invite_elevated = accepted_invite.status == Invitation.STATUSES.elevated
        if (
                not invite_elevated and not is_admin
                and request.method in ['update', 'partial_update', 'destroy']
        ):
            return False
        return invite_elevated or is_admin


class CircleViewSet(
        InvitableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (AuthenticatedOrAdminPermission, CirclePermission, )
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )

    def get_queryset(self):
        """Queryset for Circle management.

        Users invited to Circle's
        """
        visible_circles = [
            Invitation.STATUSES.invited,
            Invitation.STATUSES.accepted,
            Invitation.STATUSES.elevated,
        ]
        queryset = super().get_queryset().filter(
            invites__status__in=visible_circles,
        )
        if self.request.user.profile.type > Profile.TYPES.elevated:
            return queryset
        return queryset.filter(
            invites__profile_to__id=self.request.user.profile.id,
        )


class AuthenticatedAndReadOnlyPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions required:

        Admin can view all.
        Request method is in fae methods and User is authenticated.
        """
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return request.method in permissions.SAFE_METHODS and authenticated

    def has_object_permission(self, request, view, obj):
        """Permissions to manage access to an invited to Circle model."""
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return request.method in permissions.SAFE_METHODS and authenticated


class CircleInvitedViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (AuthenticatedAndReadOnlyPermission, )
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )

    def get_queryset(self):
        """Queryset for invited to Circle management.

        Circles the user is invited to which are not accepted.
        """
        queryset = super().get_queryset().filter(
            invites__status=Invitation.STATUSES.invited,
        )
        if self.request.user.profile.type > Profile.TYPES.elevated:
            return queryset
        return queryset.filter(
            invites__profile_to__id=self.request.user.profile.id,
        )


class CircleRejectedViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (AuthenticatedAndReadOnlyPermission, )
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )

    def get_queryset(self):
        """Queryset for invited to Circle management.

        Circles the user is invited to which are not accepted.
        """
        queryset = super().get_queryset().filter(
            invites__status=Invitation.STATUSES.rejected,
        )
        if self.request.user.profile.type > Profile.TYPES.elevated:
            return queryset
        return queryset.filter(
            invites__profile_to__id=self.request.user.profile.id,
        )


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
