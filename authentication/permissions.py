"""Policies for models and serializers."""

import logging

from rest_framework import permissions

from authentication.models import Profile


logger = logging.getLogger(__name__)


class AuthenticatedOrAdminPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions required are an authenticated user or admin."""
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated


class AuthenticatedAndReadOnlyPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions required:

        Admin can view all.
        Request method is in safe methods and User is authenticated.
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


class NoCreatePermission(permissions.AllowAny):

    def has_permission(self, request, view):
        """Not allowing create methods."""
        return view.action not in ['create', ]
