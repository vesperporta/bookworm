import pytest
from django.utils.translation import activate
from rest_framework.test import APIClient

from authentication.tests import UserFactory


@pytest.fixture(autouse=True)
def set_default_language():
    activate('en')

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def profile():
    user = UserFactory()
    return user.profile

@pytest.fixture
def profile_admin():
    user = UserFactory(is_superuser=True)
    return user.profile

@pytest.fixture
def client_profile(profile):
    client = APIClient()
    client.force_authenticate(profile.user)
    return client

@pytest.fixture
def client_admin(profile):
    client = APIClient()
    client.force_authenticate(profile.user)
    return client
