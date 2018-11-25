"""Authentication End to End tests."""

from faker import Faker

from authentication.tests import UserFactory

fake = Faker()


def test_invitation_creation(client):
    """Creation of an Invitation fails."""
    pass


def test_invitation_admin_creation(client_profile):
    """Creation of an Invitation fails for an admin."""
    pass
