"""Read Answer End to End tests."""

from faker import Faker

fake = Faker()


def test_post_create():
    """Creating a Post object as authenticated Profile."""
    pass


def test_post_owner_edit():
    """Editing a Post as owner."""
    pass


def test_post_admin_edit():
    """Editing a Post as admin."""
    pass


def test_post_notowner_edit():
    """Editing a Post neither as admin or owner fails."""
    pass


def test_post_search():
    """Searching for Posts allowed by anyone."""
    pass


def test_post_search_with_children():
    """Searching for Posts provides a minimum preview of Posts."""
    pass


def test_post_search_by_parent():
    """Searching for Posts by the parent Post provides full list of Posts."""
    pass
