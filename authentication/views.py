"""Books app views."""

from rest_framework import (viewsets, filters)

from authentication.models import (
    ContactMethod,
    Profile,
    Author,
    AuthorContactMethod,
)
from authentication.serializers import (
    ContactMethodSerializer,
    AuthorContactMethodSerializer,
    ProfileSerializer,
    AuthorSerializer,
    CircleSerializer,
    InvitationSerializer,
)
from authentication.models_circles import (
    Circle,
    Invitation,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'name_first',
        'name_last',
        'email',
    )


class ContactMethodViewSet(viewsets.ModelViewSet):
    queryset = ContactMethod.objects.all()
    serializer_class = ContactMethodSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail',)


class AuthorContactMethodViewSet(viewsets.ModelViewSet):
    queryset = AuthorContactMethod.objects.all()
    serializer_class = AuthorContactMethodSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('detail',)


class CircleViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )


class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
