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
        'profile__user__username__icontains',
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
        'profile__user__username__icontains',
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
        'profile__user__username__icontains',
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
        'count_books',
    )
    search_fields = (
        'title',
        'book__title',
        'profile__user__username__icontains',
    )
    list_filter = (
        'title',
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
    )
    search_fields = (
        'difficulty',
        'copy__icontains',
        'book__title__icontains',
        'chapter__title__icontains',
        'profile__user__username__icontains',
    )
    list_filter = ()
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
        'is_answer',
        'copy',
    )
    search_fields = (
        'is_answer',
        'copy__icontains',
        'profile__user__username__icontains',
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
        'profile__user__username__icontains',
    )
    list_filter = (
        'book',
    )
    exclude = (
        'created_at',
        'modified_at',
        'deleted_at',
    )
