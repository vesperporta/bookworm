"""Images End to End tests."""

from faker import Faker

fake = Faker()


def test_book_image_add():
    """Adding an Image object to a Book."""
    pass


def test_book_image_add_as_list():
    """Adding a group of Image objects to a Book."""
    pass


def test_book_image_add_already_added():
    """Adding an Image object to a Book already added fails."""
    pass


def test_book_image_add_primary():
    """Adding an Image object to a Book as primary overrides other selection."""
    pass


def test_book_image_remove():
    """Removing an Image object from a Book."""
    pass


def test_book_image_remove_list():
    """Removing a list of Image objects from a Book."""
    pass


def test_book_image_remove_not_added():
    """Removing an Image object from a Book not allocated to Book."""
    pass
