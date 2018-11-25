"""Reading List End to End tests."""

from faker import Faker

fake = Faker()


def test_reading_list_creation():
    """Any Profile can view ReadingList objects."""
    pass


def test_reading_list_search():
    """Anyone can view ReadingList searches."""
    pass


def test_reading_list_owner_add_book():
    """Books can be added to the ReadingList by owner of list."""
    pass


def test_reading_list_admin_add_book():
    """Books can be added to the ReadingList by owner of list as admin."""
    pass


def test_reading_list_notowner_add_book():
    """Adding a book fails when a Profile not the owner actions."""
    pass


def test_reading_list_owner_remove_book():
    """Books can be removed from the ReadingList by owner of list."""
    pass


def test_reading_list_admin_remove_book():
    """Books can be removed from the ReadingList by admin."""
    pass


def test_reading_list_notowner_remove_book():
    """Removing a book fails actioned by not the owner."""
    pass
