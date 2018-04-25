"""Books admin."""

from django.contrib import admin

from books.models import (
    Book,
    BookProgress,
    BookReview,
    BookChapter,
    ReadingList,
)
from books.models_read import (
    Thrill,
    ConfirmReadQuestion,
    ConfirmReadAnswer,
    Read,
)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin."""

    list_display = (
        'id',
        'title',
        'description',
    )
    search_fields = (
        'title__icontains',
        'description__icontains',
        'chapters__title__icontains',
        'meta_info__tags__copy__icontains',
    )
    list_filter = ('title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(BookProgress)
class BookProgressAdmin(admin.ModelAdmin):
    """BookProgress admin."""

    list_display = (
        'id',
        'book',
        'profile',
    )
    search_fields = (
        'book__title',
        'profile__user__username',
    )
    list_filter = ('book__title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    """BookProgress admin."""

    list_display = (
        'id',
        'book',
        'title',
        'progress',
    )
    search_fields = (
        'book__title',
        'profile__user__username',
        'title',
    )
    list_filter = ('title', 'book__title',)
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """BookReview admin."""

    list_display = (
        'id',
        'book',
    )
    search_fields = (
        'book__title',
        'profile__user__username',
    )
    list_filter = (
        'book__title',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    """BookReview admin."""

    list_display = (
        'id',
        'title',
        'count',
    )
    search_fields = (
        'title',
        'book__title',
        'profile__user__username',
    )
    list_filter = (
        'title',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Thrill)
class ThrillAdmin(admin.ModelAdmin):
    """Thrill admin."""

    list_display = (
        'id',
        'book',
        'reading_list',
    )
    search_fields = (
        'title__icontains',
        'book__title__icontains',
        'reading_list__title__icontains',
        'profile__user__username',
    )
    list_filter = (
        'book__title',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(ConfirmReadQuestion)
class ConfirmReadQuestionAdmin(admin.ModelAdmin):
    """ConfirmReadQuestion admin."""

    list_display = (
        'id',
        'difficulty',
        'book',
        'chapter',
        'question',
    )
    search_fields = (
        'difficulty',
        'question__icontains',
        'book__title__icontains',
        'chapter__title__icontains',
        'profile__user__username',
    )
    list_filter = (
        'question',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(ConfirmReadAnswer)
class ConfirmReadAnswerAdmin(admin.ModelAdmin):
    """ConfirmReadAnswer admin."""

    list_display = (
        'id',
        'question',
        'answer',
        'copy',
    )
    search_fields = (
        'question__icontains',
        'answer',
        'copy__icontains',
        'profile__user__username',
    )
    list_filter = (
        'copy',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )


@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    """Read admin."""

    list_display = (
        'id',
        'book',
        'answered_correctly',
    )
    search_fields = (
        'book__title__icontains',
        'question__copy__icontains',
        'profile__user__username',
    )
    list_filter = (
        'book',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
