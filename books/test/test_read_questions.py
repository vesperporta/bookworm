"""Read Questions End to End tests."""

from faker import Faker

fake = Faker()


def test_read_questions_create():
    """Profile.TYPES.elevated authorization allowed to create."""
    pass


def test_read_questions_search():
    """Any authorization allowed to create."""
    pass


def test_read_questions_elevated_edit():
    """Elevated authorization able to edit a ReadQuestion."""
    pass


def test_read_questions_admin_edit():
    """Admin authorization able to edit a ReadQuestion."""
    pass


def test_read_questions_normal_edit_fails():
    """Normal authorization fails to edit a ReadQuestion."""
    pass
