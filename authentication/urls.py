from django.conf.urls import url

from rest_framework import routers
from rest_framework_jwt.views import (
    refresh_jwt_token,
    verify_jwt_token,
    ObtainJSONWebToken,
)

from authentication.views import (
    ProfileViewSet,
    ProfileMeViewSet,
    AuthorViewSet,
    ContactMethodViewSet,
    CircleViewSet,
    InvitationViewSet,
)
from authentication.serializers_jwt import UsernameEmailJWTSerializer


router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'contact', ContactMethodViewSet)
router.register(r'circle', CircleViewSet)
router.register(r'invitation', InvitationViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(
        r'^token-auth/',
        ObtainJSONWebToken.as_view(serializer_class=UsernameEmailJWTSerializer)
    ),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(
        r'me/',
        ProfileMeViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', },
        )
    )
]
