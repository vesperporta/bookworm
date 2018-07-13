"""Authentication view sets."""

from rest_framework import (viewsets, filters, permissions)

from authentication.permissions import (
    AuthenticatedOrAdminPermission,
    AuthenticatedAndReadOnlyPermission,
)
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
from authentication.views_invitable import InvitableViewSetMixin


class ProfilePermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions for the Profile view.

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
        'contacts__detail',
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


class AuthorPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Author objects are viewable by all.

        User authentication required otherwise.
        Admins can do all actions.
        """
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        if view.action in ['list', 'retrieve', ]:
            return True
        return authenticated

    def has_object_permission(self, request, view, obj):
        """Authentication required to update an author.

        Owners of an Author are able to update that author.
        Admins can do all actions.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated and obj.profile.id == request.user.profile.id


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (AuthorPermission, )
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'name_first',
        'name_last',
        'contacts__detail',
    )


class ContactMethodPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """ContactMethod object permissions.

        Non admins can only interact with ContactMethod's associated with
        their own Profile.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated and obj.profile.contacts.filter(id__in=[obj.id])


class ContactMethodViewSet(viewsets.ModelViewSet):
    queryset = ContactMethod.objects.all()
    serializer_class = ContactMethodSerializer
    permission_classes = (
        AuthenticatedOrAdminPermission,
        ContactMethodPermission,
    )
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'detail',
    )

    def get_queryset(self):
        """ContactMethod queryset.

        Non admins only see their own ContactMethods.
        """
        queryset = super().get_queryset()
        if (
                self.action in ['list', 'retrieve', ]
                and self.request.user.profile.type < Profile.TYPES.admin
        ):
            return self.request.user.profile.contacts.all()
        return queryset


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


class CircleViewSet(InvitableViewSetMixin, viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (
        AuthenticatedOrAdminPermission,
        CirclePermission,
    )
    filter_backends = (filters.SearchFilter, )
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


class CircleInvitedViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (AuthenticatedAndReadOnlyPermission, )
    filter_backends = (filters.SearchFilter, )
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
    filter_backends = (filters.SearchFilter, )
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
