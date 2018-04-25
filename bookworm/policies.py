"""Policies for models and serializers."""

# from django_common.auth_backends import User

from dry_rest_permissions.generics import authenticated_users

from authentication.models import Profile


class AnyPermisionsMixin:
    """Allow all permisions to model."""

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        """
        We can remove the has_create_permission because this implicitly grants that permission.
        """
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner


class MembersReadOnlyPermsMixin:
    """Make the endpoint only editable by editors."""

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        """Check permissions for GET requests.

        Make object readable for all authenticated users.
        """
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        """Check permissions for GET requests over specific instance.

        All authenticated users can do that.
        """
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for POST/PUT/PATCH/DELETE requests.

        Only editors can modify the inventory.
        """
        types = (
            Profile.TYPES.elevated,
            Profile.TYPES.admin,
            Profile.TYPES.destroyer,
        )
        return request.user.profile.type in types

    @authenticated_users
    def has_object_write_permission(self, request):
        """Check permissions for POST/PUT/PATCH/DELETE requests.

        Only editors can modify the inventory.
        """
        types = (
            Profile.TYPES.elevated,
            Profile.TYPES.admin,
            Profile.TYPES.destroyer,
        )
        return request.user.profile.type in types


class MemberCreateReadPermissions:
    """Permissions for member activities.

    Allow members to read and create their activities.
    """

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        """Check permissions for GET requests.

        It doesn't check anything because it's checked in has_list_permission
        and has_object_read_permission.
        """
        return True

    @staticmethod
    @authenticated_users
    def has_list_permission(request):
        """Check permissions for GET request on /v1/<endpoint>/."""
        if request.user.is_superuser:
            return True

        try:
            query_id = int(request.query_params['member_profile'])
        except (KeyError, ValueError):
            # member_profile not set or is not an integer
            return False

        if request.user.type == 'delegate_member':
            member_profile_id = request.user.delegate_member.member_profile.id
        else:
            member_profile_id = request.user.member_profile.id
        return query_id == member_profile_id

    @authenticated_users
    def has_object_read_permission(self, request):
        """Check permissions for GET request on /v1/<endpoint>/<ID>/.

        Only has permissions if the user is a superuser or if it is a member or
        a delegate member of the user that is trying to access.
        """
        if request.user.is_superuser:
            return True
        if (request.user.type == 'delegate_member' and
                request.user.delegate_member.member_profile ==
                self.member_profile):
            return True
        return request.user == self.member_profile.user

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for POST/PUT/PATCH/DELETE requests.

        Only allow POST (the serializer manage to only allow create activities
        for the current member).
        """
        if request.method == 'POST':
            return True
        return False


class MemberCreateReadUpdatePermissions(MemberCreateReadPermissions):
    """Permissions for member activities.

    Allow members to read, create and update their activities.
    """

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        """Check permissions for POST/PATCH requests.

        Allow POST and PATCH (the serializer manage to only allow create
        and update activities for the current member).
        """
        if request.method == 'POST' or request.method == 'PATCH':
            return True
        return False

    @authenticated_users
    def has_object_write_permission(self, request):
        """Check permissions for PUT/PATCH/DELETE request on /v1/<endpoint>/<ID>/.

        Only has permissions if the user is a superuser or if it is a member or
        a delegate member of the user that is trying to access.
        """
        if request.user.is_superuser:
            return True
        if (request.user.type == 'delegate_member' and
                request.user.delegate_member.member_profile ==
                self.member_profile):
            return True
        return request.user == self.member_profile.user
