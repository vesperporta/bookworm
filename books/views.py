"""Books app views."""

from rest_framework import (viewsets, filters)

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
from books.serializers import (
    BookSerializer,
    BookProgressSerializer,
    BookReviewSerializer,
    BookChapterSerializer,
    ReadingListSerializer,
    ThrillSerializer,
    BookThrillSerializer,
    ReadingListThrillSerializer,
    ConfirmReadQuestionSerializer,
    ConfirmReadAnswerSerializer,
    ReadSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class BookProgressViewSet(viewsets.ModelViewSet):
    queryset = BookProgress.objects.all()
    serializer_class = BookProgressSerializer

    def create(self, request, *args, **kwargs):
        # Test for REVIEW data available
        return super().create(request, *args, **kwargs)


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer

    def create(self, request, *args, **kwargs):
        # Test for progress data available
        return super().create(request, *args, **kwargs)


class BookChapterViewSet(viewsets.ModelViewSet):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterSerializer


class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer


class ThrillViewSet(viewsets.ModelViewSet):
    queryset = Thrill.objects.all()
    serializer_class = ThrillSerializer


class BookThrillViewSet(viewsets.ModelViewSet):
    queryset = Thrill.objects.all()
    serializer_class = BookThrillSerializer


class ReadingListThrillViewSet(viewsets.ModelViewSet):
    queryset = Thrill.objects.all()
    serializer_class = ReadingListThrillSerializer


class ConfirmReadQuestionViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadQuestion.objects.all()
    serializer_class = ConfirmReadQuestionSerializer


class ConfirmReadAnswerViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadAnswer.objects.all()
    serializer_class = ConfirmReadAnswerSerializer


class ReadViewSet(viewsets.ModelViewSet):
    queryset = Read.objects.all()
    serializer_class = ReadSerializer
