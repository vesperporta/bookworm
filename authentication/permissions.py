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
