from rest_framework import routers

from posts.views import (
    EmoteViewSet,
    PostViewSet,
    CommentViewSet,
)


router = routers.SimpleRouter()
router.register(r'emote', EmoteViewSet)
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = router.urls
