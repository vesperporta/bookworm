from rest_framework import routers

from authentication.views import (
    ProfileViewSet,
    ContactMethodViewSet,
)


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'contact', ContactMethodViewSet)

urlpatterns = router.urls
