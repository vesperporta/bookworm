"""Images End to End tests."""

from faker import Faker

fake = Faker()


"""Profile tests"""


def test_profile_image_add():
    """Adding an Image object to a Profile."""
    pass


def test_profile_image_add_as_list():
    """Adding a group of Image objects to a Profile."""
    pass


def test_profile_image_add_already_added():
    """Adding an Image object to a Profile already added fails."""
    pass


def test_profile_image_add_primary():
    """Adding an Image object to a Profile as primary overrides other selection.
    """
    pass


def test_profile_image_remove():
    """Removing an Image object from a Profile."""
    pass


def test_profile_image_remove_list():
    """Removing a list of Image objects from a Profile."""
    pass


def test_profile_image_remove_not_added():
    """Removing an Image object from a Book not allocated to Profile."""
    pass


"""Author tests"""


def test_author_image_add():
    """Adding an Image object to an Author."""
    pass


def test_author_image_add_as_list():
    """Adding a group of Image objects to an Author."""
    pass


def test_author_image_add_already_added():
    """Adding an Image object to an Author already added fails."""
    pass


def test_author_image_add_primary():
    """Adding an Image object to an Author as primary overrides other selection.
    """
    pass


def test_author_image_remove():
    """Removing an Image object from an Author."""
    pass


def test_author_image_remove_list():
    """Removing a list of Image objects from an Author."""
    pass


def test_author_image_remove_not_added():
    """Removing an Image object from an Author not allocated to Profile."""
    pass
