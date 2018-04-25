"""Books app views."""

from rest_framework import (viewsets, filters)
from dry_rest_permissions.generics import DRYPermissions

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
    ConfirmReadQuestionSerializer,
    ConfirmReadAnswerSerializer,
    ReadSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    permission_classes = (DRYPermissions,)


class BookProgressViewSet(viewsets.ModelViewSet):
    queryset = BookProgress.objects.all()
    serializer_class = BookProgressSerializer
    permission_classes = (DRYPermissions,)

    def create(self, request, *args, **kwargs):
        # Test for REVIEW data available
        return super().create(request, *args, **kwargs)


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = (DRYPermissions,)

    def create(self, request, *args, **kwargs):
        # Test for progress data available
        return super().create(request, *args, **kwargs)


class BookChapterViewSet(viewsets.ModelViewSet):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterSerializer
    permission_classes = (DRYPermissions,)


class ReadingListViewSet(viewsets.ModelViewSet):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer
    permission_classes = (DRYPermissions,)


class ThrillViewSet(viewsets.ModelViewSet):
    queryset = Thrill.objects.all()
    serializer_class = ThrillSerializer
    permission_classes = (DRYPermissions,)


class ConfirmReadQuestionViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadQuestion.objects.all()
    serializer_class = ConfirmReadQuestionSerializer
    permission_classes = (DRYPermissions,)


class ConfirmReadAnswerViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadAnswer.objects.all()
    serializer_class = ConfirmReadAnswerSerializer
    permission_classes = (DRYPermissions,)


class ReadViewSet(viewsets.ModelViewSet):
    queryset = Read.objects.all()
    serializer_class = ReadSerializer
    permission_classes = (DRYPermissions,)
