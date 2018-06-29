"""Books admin."""

from django.contrib import admin
from authentication.models import (
    Profile,
    ProfileSetting,
    ContactMethod,
)
from authentication.models_circles import (
    Circle,
    CircleSetting,
    Invitation,
)


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'id',
        'type',
        'detail',
        'email',
        'uri',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = (
        'id',
        'name_first',
        'name_family',
        'name_display',
        'email',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
    readonly_fields = (
        'user',
    )


@admin.register(ProfileSetting)
class ProfileSettingAdmin(admin.ModelAdmin):
    """ProfileSetting admin."""

    list_display = (
        'id',
        'copy',
        'json',
    )
    readonly_fields = (
        'profile',
    )
    search_fields = (
        'copy',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin."""

    list_display = (
        'id',
        'title',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
    readonly_fields = (
        'invites',
    )


@admin.register(CircleSetting)
class CircleSettingAdmin(admin.ModelAdmin):
    """CircleSetting admin."""

    list_display = (
        'id',
        'copy',
        'json',
    )
    readonly_fields = (
        'circle',
    )
    search_fields = (
        'copy',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """Invitation admin."""

    list_display = (
        'id',
        'status',
        'profile',
        'profile_to',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
    readonly_fields = (
    )
