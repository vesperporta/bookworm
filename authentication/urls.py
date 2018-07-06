from django.conf.urls import url

from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from authentication.views import (
    ProfileViewSet,
    AuthorViewSet,
    ContactMethodViewSet,
    CircleViewSet,
    InvitationViewSet,
)


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'contact', ContactMethodViewSet)
router.register(r'circle', CircleViewSet)
router.register(r'invitation', InvitationViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
]
