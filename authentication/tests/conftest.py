import pytest
from django.utils.translation import activate
from rest_framework.test import APIClient

from authentication.tests import UserFactory


@pytest.fixture(autouse=True)
def set_default_language():
    """Unless otherwise specified set the localisation to English."""
    activate('en')

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Automatically support database access to any tests requiring."""
    pass

@pytest.fixture
def profile():
    """Normal user and profile account."""
    user = UserFactory()
    return user.profile

@pytest.fixture
def profile_admin():
    """Administration user and profile."""
    user = UserFactory(is_superuser=True)
    return user.profile

@pytest.fixture
def client_profile(profile):
    """API Client authenticated as a user."""
    client = APIClient()
    client.force_authenticate(profile.user)
    return client

@pytest.fixture
def client_admin(profile_admin):
    """API Client authenticated as an administrator."""
    client = APIClient()
    client.force_authenticate(profile_admin.user)
    return client
