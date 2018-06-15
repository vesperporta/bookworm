"""FileStore urls """

from rest_framework import routers

from file_store.views import (
    ImageViewSet,
    DocumentViewSet,
)


router = routers.SimpleRouter()
router.register(r'image', ImageViewSet)
router.register(r'document', DocumentViewSet)

urlpatterns = router.urls
