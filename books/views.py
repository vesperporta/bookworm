"""Books app views."""

import logging

from rest_framework import (status, viewsets, filters)
from rest_framework.decorators import detail_route
from rest_framework.response import Response

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
from books.serializers import (
    BookSerializer,
    BookProgressSerializer,
    BookReviewSerializer,
    BookChapterSerializer,
    ReadingListSerializer,
    ConfirmReadQuestionSerializer,
    ConfirmReadAnswerSerializer,
    ReadSerializer,
)
from books.exceptions import BookRequiredValidation
from posts.views import EmotableViewSet
from file_store.views import ImagableViewSet
from meta_info.views import LocalisableViewSetMixin

logger = logging.getLogger(__name__)


class BookViewSet(
        EmotableViewSet,
        ImagableViewSet,
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', )


class BookProgressViewSet(viewsets.ModelViewSet):
    queryset = BookProgress.objects.all()
    serializer_class = BookProgressSerializer


class BookReviewViewSet(
        EmotableViewSet,
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy', 'book__title', )


class BookChapterViewSet(
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'book__title', )


class ReadingListViewSet(
        EmotableViewSet,
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'books__title', )

    def _book_error_handle(self, reading_list, error):
        """Handle error responses from reading list.

        @param reading_list: ReadingList object.
        @param error: Exeption object.

        @return Response with 400 status code.
        """
        return Response(
            {
                'status': 'error',
                'ok': '💩',
                'reading_list': reading_list.id,
                'error': error.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @detail_route(methods=['post'])
    def add_book(self, request, pk, **kwargs):
        """Add a book to a ReadingList object."""
        reading_list = self.get_object()
        book_id = request.data.get('book')
        if not book_id:
            self._book_error_handle(
                reading_list,
                BookRequiredValidation('book'),
            )
        try:
            reading_list.add_book(book_id)
        except Book.DoesNotExist as error:
            return self._book_error_handle(reading_list, error)
        return Response(
            {
                'status': 'added',
                'ok': '🖖',
                'reading_list': reading_list.id,
                'book': request.POST.get('book'),
            }
        )

    @detail_route(methods=['post'])
    def remove_book(self, request, pk, **kwargs):
        """Remove a book from a ReadingList object."""
        reading_list = self.get_object()
        book_id = request.data.get('book')
        if not book_id:
            self._book_error_handle(
                reading_list,
                BookRequiredValidation('book'),
            )
        try:
            reading_list.remove_book(book_id)
        except Book.DoesNotExist as error:
            return self._book_error_handle(reading_list, error)
        return Response(
            {
                'status': 'removed',
                'ok': '🖖',
                'reading_list': reading_list.id,
                'book': request.POST.get('book'),
            }
        )


class ConfirmReadQuestionViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = ConfirmReadQuestion.objects.all()
    serializer_class = ConfirmReadQuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('book__title', 'copy', )


class ConfirmReadAnswerViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadAnswer.objects.all()
    serializer_class = ConfirmReadAnswerSerializer


class ReadViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Read.objects.all()
    serializer_class = ReadSerializer
