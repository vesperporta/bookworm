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
from posts.views import EmotableViewSet

logger = logging.getLogger(__name__)


class BookViewSet(
        EmotableViewSet,
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
        viewsets.ModelViewSet,
):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy', 'book__title', )


class BookChapterViewSet(viewsets.ModelViewSet):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'book__title', )


class ReadingListViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'books__title', )

    @detail_route(methods=['post'])
    def add_book(self, request, pk, **kwargs):
        reading_list = self.get_object()
        response = {
            'status': 'added',
            'reading_list': reading_list.id,
            'book': request.POST.get('book'),
        }
        try:
            reading_list.add_book(request.POST.get('book'))
        except Book.DoesNotExist as e:
            response.update({
                'status': 'error',
                'error': e.detail,
            })
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(response)

    @detail_route(methods=['post'])
    def remove_book(self, request, pk, **kwargs):
        reading_list = self.get_object()
        response = {
            'status': 'removed',
            'reading_list': reading_list.id,
            'book': request.POST.get('book'),
        }
        try:
            reading_list.remove_book(request.POST.get('book'))
        except Book.DoesNotExist as e:
            response.update({
                'status': 'error',
                'error': e.detail,
            })
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(response)


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
