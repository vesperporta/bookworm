"""Authentication End to End tests."""

from faker import Faker

from authentication.tests import UserFactory

fake = Faker()


def test_circle_search_public(client):
    """Public visibility as unauthenticated user errors."""
    pass


def test_circle_create(client_profile):
    """Authenticated users can create a Circle."""
    pass


def test_circle_search(client_profile):
    """Authenticated users can view Circles they are invited and accepted to."""
    pass


def test_circle_invite_profile(client_profile):
    """Invite a Profile to be part of a Circle."""
    pass


def test_circle_update_unauthorised(client_admin):
    """Updating a circle not authorised as Invitation.STATUSES.accepted"""
    pass


def test_circle_search_banned(client_profile):
    """Searching for a Circle user is banned from fails."""
    pass


def test_circle_withdrawn_profiles(client_profile):
    """Viewing of withdrawn profiles requires Invitation.STATUSES.elevated"""
    pass
