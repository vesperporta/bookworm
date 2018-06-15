"""FileStore admin."""

from django.contrib import admin

from file_store.models import (
    Image,
    Document,
)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Image admin."""

    list_display = (
        'id',
        'title',
        'source_url'
    )
    search_fields = (
        'title',
        'description',
        'tags__copy',
    )
    list_filter = ('title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document admin."""

    list_display = (
        'id',
        'title',
        'description',
        'file',
    )
    search_fields = (
        'title',
        'tags__copy',
    )
    list_filter = ('title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
