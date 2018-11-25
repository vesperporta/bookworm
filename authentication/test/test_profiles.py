"""Authentication End to End tests."""

from faker import Faker

from authentication.test import UserFactory

fake = Faker()
expected_no_permission = 'You do not have permission to perform this action.'


def test_me_unauthenticated(client):
    """Assertion to get a profile without authentication."""
    expected = 'Authentication credentials were not provided.'
    response = client.post('/authentication/me/')
    assert response.json()['detail'] == expected


def test_me(client_profile, profile):
    """Ensure an authenticated profile is getting their information.

    Note: the email on Profile is marked unique on database level.
    """
    response = client_profile.get('/authentication/me/')
    assert response.json()['email'] == profile.email


def test_profile_from_id(client_profile, profile):
    """Validate the profile can see their information using their URI."""
    response = client_profile.get(f'/authentication/profile/{profile.id}/')
    assert response.json()['email'] == profile.email


def test_profile_from_id_not_authenticated_as_profile(client_profile):
    """Using another Profile URI assert their information is not vissible.

    Note: subject to change when public visibility is implemented, this will
    then require field level inspection of visibility.
    """
    user = UserFactory()
    response = client_profile.get(f'/authentication/profile/{user.profile.id}/')
    assert response.json()['detail'] == expected_no_permission


def test_profile_create(client):
    """Create a Profile and User without being authenticated."""
    data = {
        'email': fake.email(),
        'password': fake.password(),
        'name_title': 1,
        'name_first': fake.first_name(),
        'name_family': fake.last_name(),
        'name_display': fake.user_name(),
    }
    response = client.post('/authentication/profile/', data)
    assert response.json()['email'] == data['email']


def test_profile_create_while_authenticated(client_profile):
    """Fail an attempt to create a Profile and User while authenticated."""
    data = {
        'email': fake.email(),
        'password': fake.password(),
        'name_title': 1,
        'name_first': fake.first_name(),
        'name_family': fake.last_name(),
        'name_display': fake.user_name(),
    }
    response = client_profile.post('/authentication/profile/', data)
    assert response.json()['detail'] == expected_no_permission
