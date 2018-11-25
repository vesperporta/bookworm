"""Tags End to End tests."""

from faker import Faker

fake = Faker()


def test_tag_create():
    """Creating a Tag object."""
    pass


def test_tag_edit():
    """Editing a Tag object."""
    pass


def test_tag_elevated_delete():
    """Deleting a Tag object as elevated."""
    pass


def test_tag_admin_delete():
    """Deleting a Tag object as admin."""
    pass


def test_tag_notelevated_notadmin_delete():
    """Deleting a Tag object not as admin or elevated Profile."""
    pass
