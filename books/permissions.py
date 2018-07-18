"""Books policies."""

import logging

from rest_framework import permissions

from authentication.models import Profile

logger = logging.getLogger(__name__)


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """Permissions for read only.

        Actions in the SAFE_METHODS list are allowed.
        Admins are able to manage Read objects normally.
        """
        if request.user.profile.type >= Profile.TYPES.admin:
            return True
        return request.method in permissions.SAFE_METHODS


class ElevatedCreateEditPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions for elevated users and admin.

        Profiles with elevated and above status are only allowed.
        """
        authenticated = super().has_permission(request, view)
        if request.method not in permissions.SAFE_METHODS:
            if authenticated:
                return request.user.profile.type >= Profile.TYPES.elevated
            return False
        return authenticated


class AnyReadOrElevatedPermission(permissions.AllowAny):

    def has_permission(self, request, view):
        """Allow any user to read or elevated Profile status and above."""
        if request.method not in permissions.SAFE_METHODS:
            if request.user and request.user.is_authenticated:
                return request.user.profile.type >= Profile.TYPES.elevated
        return True


class AnyReadOwnerCreateEditPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Profiles owning this object may only edit or delete."""
        if request.method in permissions.SAFE_METHODS:
            return True
        authenticated = super().has_object_permission(request, view, obj)
        return authenticated and obj.profile.id == request.user.profile.id


class OwnerAndAdminPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Owner and admin have access."""
        authenticated = super().has_permission(request, view)
        return (
            authenticated and
            (
                obj.profile.id == request.user.profile.id or
                request.user.profile.type >= Profile.TYPES.admin
            )
        )
