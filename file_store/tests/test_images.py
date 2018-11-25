"""Documents End to End tests."""

from faker import Faker

fake = Faker()


def test_image_create():
    """Images can be created by authenticated Profiles."""
    pass


def test_image_search():
    """Anyone can view Images."""
    pass


def test_image_admin_edit():
    """Administrators can edit an Image."""
    pass


def test_image_notadmin_edit():
    """Image modifications fail for unauthorized Profiles."""
    pass
