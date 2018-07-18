"""Books app views."""

import logging

from rest_framework import (status, viewsets, filters, permissions, decorators)
from rest_framework.response import Response

from authentication.models import Profile
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
from books.permissions import (
    ReadOnlyPermission,
    ElevatedCreateEditPermission,
    AnyReadOrElevatedPermission,
    AnyReadOwnerCreateEditPermission,
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
from books.exceptions import (
    BookRequiredValidation,
    AnswerAlreadyAcceptedValidation,
    CannotAcceptOwnAnswerValidation,
)
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
    permission_classes = (AnyReadOrElevatedPermission, )


class BookProgressViewSet(viewsets.ModelViewSet):
    queryset = BookProgress.objects.all()
    serializer_class = BookProgressSerializer
    permission_classes = (AnyReadOwnerCreateEditPermission, )


class BookReviewViewSet(
        EmotableViewSet,
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('copy', 'book__title', )
    permission_classes = (AnyReadOwnerCreateEditPermission, )


class BookChapterViewSet(
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'book__title', )
    permission_classes = (AnyReadOrElevatedPermission, )


class ReadingListViewSet(
        EmotableViewSet,
        LocalisableViewSetMixin,
        viewsets.ModelViewSet,
):
    queryset = ReadingList.objects.all()
    serializer_class = ReadingListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'books__title', )
    permission_classes = (AnyReadOwnerCreateEditPermission, )

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

    @decorators.detail_route(methods=['post'])
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

    @decorators.detail_route(methods=['post'])
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
    permission_classes = (ElevatedCreateEditPermission, )


class ConfirmReadAnswerPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """Users may only update their own answers.

        Admins are allowed to update any answer.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated and obj.profile.id == request.user.profile.id


class ConfirmReadAnswerAcceptPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        """Permissions to allow specific status Profiles.

        Authenticated and elevated and above status Profiles.
        """
        return (
                super().has_permission(request, view) and
                request.user.profile.type >= Profile.TYPES.elevated
        )

    def has_object_permission(self, request, view, obj):
        """Users may not accept their own answer.

        Admins are allowed to accept their own answers.
        """
        authenticated = super().has_object_permission(request, view, obj)
        if authenticated:
            if request.user.profile.type >= Profile.TYPES.admin:
                return True
        return authenticated and obj.profile.id != request.user.profile.id


class ConfirmReadAnswerViewSet(viewsets.ModelViewSet):
    queryset = ConfirmReadAnswer.objects.all()
    serializer_class = ConfirmReadAnswerSerializer
    permission_classes = (ConfirmReadAnswerPermission, )

    @decorators.detail_route(methods=['post'])
    @decorators.permission_classes((ConfirmReadAnswerAcceptPermission, ))
    def accept(self, request, pk, **kwargs):
        """Accept this answer."""
        answer = self.get_object()
        try:
            answer.accept_answer(request.user.profile)
        except (
                AnswerAlreadyAcceptedValidation,
                CannotAcceptOwnAnswerValidation,
        ) as error:
            return Response(
                {
                    'status': 'error',
                    'ok': '💩',
                    'error': error.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                'status': 'accepted',
                'ok': '🕶',
            }
        )


class ReadViewSet(
        EmotableViewSet,
        viewsets.ModelViewSet,
):
    queryset = Read.objects.all()
    serializer_class = ReadSerializer
    permission_classes = (permissions.IsAuthenticated, ReadOnlyPermission, )
