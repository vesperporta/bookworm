"""Books policies."""

import logging

from django.conf import settings

from dry_rest_permissions.generics import authenticated_users


logger = logging.getLogger(__name__)


class OpenPolicyMixin:
    """Policy definition for open access."""

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
        return True

    @staticmethod
    @authenticated_users
    def has_create_permission(request):
        """Check permissions for POST request on list."""
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for PUT/PATCH/DELETE requests."""
        return True

    @authenticated_users
    def has_object_update_permission(self, request):
        """Detail update permissions."""
        return True

    @authenticated_users
    def has_object_destroy_permission(self, request):
        """Check permissions for DELETE request on detail."""
        return True


class OwnerElevatedAndLockAccessMixin:
    """ConfirmReadAnswer policy

    Keep the answers secure for editing by elevated and above or
    if the answer is locked then owner and administrator.

    lock can only be modified by owner or administrator.
    """

    def _auth_core(self, request):
        return bool(
            request.user.is_superuser or
            request.user == self.profile.user
        )

    @staticmethod
    def _auth_elevated(request):
        elevated_type_min = int(settings.get('PROFILE_TYPE_ELEVATED__MIN'))
        return request.user.profile.type >= elevated_type_min

    @staticmethod
    def _auth_admin(request):
        admin_type_min = int(settings.get('PROFILE_TYPE_ADMIN__MIN'))
        return (
            request.user.profile.type >= admin_type_min or
            request.user.is_superuser
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
        return True

    @staticmethod
    @authenticated_users
    def has_create_permission(request):
        """Check permissions for POST request on list."""
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for PUT/PATCH/DELETE requests."""
        return True

    @authenticated_users
    def has_object_update_permission(self, request):
        """Detail update permissions."""
        elevated_type_min = int(settings.get('PROFILE_TYPE_ELEVATED__MIN'))
        admin_type_min = int(settings.get('PROFILE_TYPE_ADMIN__MIN'))
        core_perms = bool(
            request.user.is_superuser or
            request.user == self.profile.user
        )
        if bool(request.query_params['lock']):
            return core_perms or request.user.profile.type >= admin_type_min
        return core_perms or request.user.profile.type >= elevated_type_min

    @authenticated_users
    def has_object_destroy_permission(self, request):
        """Check permissions for DELETE request on detail."""
        admin_type_min = int(settings.get('PROFILE_TYPE_ADMIN__MIN'))
        return (
            request.user.is_superuser or
            request.user == self.profile.user or
            request.user.profile.type >= admin_type_min
        )


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
