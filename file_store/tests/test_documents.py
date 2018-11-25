"""Documents End to End tests."""

from faker import Faker

fake = Faker()


def test_document_create():
    """Documents can be created by authenticated Profiles."""
    pass


def test_document_search():
    """Anyone can view Documents."""
    pass


def test_document_admin_edit():
    """Administrators can edit a Document."""
    pass


def test_document_notadmin_edit():
    """Document modifications fail for unauthorized Profiles."""
    pass
