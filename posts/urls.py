from rest_framework import routers

from posts.views import (
    EmoteViewSet,
    PostViewSet,
)


router = routers.SimpleRouter()
router.register(r'emote', EmoteViewSet)
router.register(r'post', PostViewSet)

urlpatterns = router.urls
