"""Authentication End to End tests."""

from faker import Faker

fake = Faker()


def test_contact_method_create():
    """ContactMethods are not created directly."""
    pass


def test_contact_method_authenticated_search():
    """ContactMethods supplied are the same from Profile authenticated only."""
    pass


def test_contact_method_admin_search():
    """ContactMethods search over all objects."""
    pass


def test_contact_method_owner_edit():
    """Owner of ContactMethod can edit."""
    pass


def test_contact_method_admin_edit():
    """Admins can edit a ContactMethod or other Profile."""
    pass


def test_contact_method_notowner_edit():
    """Non owner of ContactMethod fails edit."""
    pass


def test_contact_method_owner_delete():
    """Owner of ContactMethod can delete."""
    pass


def test_contact_method_delete_is_archive():
    """On delete of a ContactMethod the object is not deleted from database.

    A flag is set and the object manager filters out flagged.
    """
    pass


def test_contact_method_notowner_delete():
    """Non owner of ContactMethod fails delete."""
    pass
