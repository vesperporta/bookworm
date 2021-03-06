"""Posts admin."""

from django.contrib import admin

from posts.models import (
    Emote,
    Post,
)


@admin.register(Emote)
class EmoteAdmin(admin.ModelAdmin):
    """Emote admin."""

    list_display = (
        'id',
        'profile',
    )
    search_fields = (
        'profile__user__username',
    )
    list_filter = ('profile',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    list_display = (
        'id',
        'profile',
        'copy',
    )
    search_fields = (
        'copy__icontains',
        'profile__user__username',
    )
    list_filter = ('profile',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
