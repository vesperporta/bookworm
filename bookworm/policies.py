"""Policies for models and serializers."""

import logging

from django.conf import settings

from dry_rest_permissions.generics import authenticated_users


logger = logging.getLogger(__name__)


class OwnerAdminAccessMixin:
    """Policy defining owner of model and admins write access.

    Default access of all others is read.
    """

    def _get_admin_grade_user_bool(self, request):
        admin_type_min = settings.get('PROFILE_TYPE_ADMIN__MIN')
        return (
            request.user.is_superuser or
            request.user == self.profile.user or
            request.user.profile.type >= admin_type_min
        )

    @staticmethod
    @authenticated_users
    def has_list_permission(request):
        """Check permissions for GET request on list."""
        return True

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        """Check permissions for GET request on detail."""
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        """Check permissions for GET request on detail."""
        return self._get_admin_grade_user_bool(request)

    @staticmethod
    @authenticated_users
    def has_create_permission(request):
        """Check permissions for POST request on list."""
        return False

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for PUT/PATCH/DELETE requests."""
        return True

    @authenticated_users
    def has_object_update_permission(self, request):
        """Detail update permissions."""
        return self._get_admin_grade_user_bool(request)

    @authenticated_users
    def has_object_destroy_permission(self, request):
        """Check permissions for DELETE request on detail."""
        return False


class ProfileOnlyAccessMixin:
    """stuff"""

    @staticmethod
    @authenticated_users
    def has_change_password_permission(request):
        """Change password permissions."""
        return True

    def has_object_change_password_permission(self, request):
        """Change object password permissions."""
        return request.user == self.profile.user

    @staticmethod
    @authenticated_users
    def has_change_email_permission(request):
        """Change email permissions."""
        return True

    def has_object_change_email_permission(self, request):
        """Change object email permissions."""
        return request.user == self.profile.user
