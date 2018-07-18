"""Books policies."""

import logging

from rest_framework import permissions

from authentication.models import Profile

logger = logging.getLogger(__name__)


class ElevatedForDeletePermission(permissions.AllowAny):

    def has_permission(self, request, view):
        """Averyone can read, elevated Profile status and above to delete."""
        if request.user.profile.type >= Profile.TYPES.elevated:
            return True
        return view.action in ['delete', ]
