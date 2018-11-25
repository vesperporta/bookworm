"""Authentication End to End tests."""

from faker import Faker

from authentication.test import UserFactory

fake = Faker()


def test_author_search_public(client):
    """Search for authors and ensure public fields are only visible."""
    pass


def test_author_search(client_profile):
    """Search for authors as authenticated user."""
    pass


def test_create_author(client_admin):
    """Create an Author as an admin"""
    pass


def test_create_author_unauthorised(client_profile):
    """Fail attempting to create an Author not an admin."""
    pass
