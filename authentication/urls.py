from rest_framework import routers

from authentication.views import (
    ProfileViewSet,
    ContactMethodViewSet,
    CircleViewSet,
    InvitationViewSet,
)


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'contact', ContactMethodViewSet)
router.register(r'circle', CircleViewSet)
router.register(r'invitation', InvitationViewSet)

urlpatterns = router.urls
