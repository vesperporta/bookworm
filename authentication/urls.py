from rest_framework import routers

from authentication.views import (
    ProfileViewSet,
    AuthorViewSet,
    ContactMethodViewSet,
    AuthorContactMethodViewSet,
    CircleViewSet,
    InvitationViewSet,
)


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'contact', ContactMethodViewSet)
router.register(r'author_contact', AuthorContactMethodViewSet)
router.register(r'circle', CircleViewSet)
router.register(r'invitation', InvitationViewSet)

urlpatterns = router.urls
