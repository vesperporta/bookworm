from rest_framework import routers

from books.views import (
    BookViewSet,
    BookProgressViewSet,
    BookReviewViewSet,
    BookChapterViewSet,
    ReadingListViewSet,
    ThrillViewSet,
    BookThrillViewSet,
    ReadingListThrillViewSet,
    ConfirmReadQuestionViewSet,
    ConfirmReadAnswerViewSet,
    ReadViewSet,
)


router = routers.SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'progress', BookProgressViewSet)
router.register(r'review', BookReviewViewSet)
router.register(r'chapter', BookChapterViewSet)
router.register(r'reading_list', ReadingListViewSet)
router.register(r'thrill', ThrillViewSet)
router.register(r'book_thrill', BookThrillViewSet)
router.register(r'reading_list_thrill', ReadingListThrillViewSet)
router.register(r'read_question', ConfirmReadQuestionViewSet)
router.register(r'read_answer', ConfirmReadAnswerViewSet)
router.register(r'read', ReadViewSet)

urlpatterns = router.urls
