"""Read Answer End to End tests."""

from faker import Faker

fake = Faker()


def test_read_answers_create():
    """Create a ReadAnswer for a ReadQuestion."""
    pass


def test_read_answers_create_no_question():
    """Create a ReadAnswer without a ReadQuestion fails."""
    pass


def test_read_answers_owner_edit():
    """Edit a ReadAnswer as owner of ReadAnswer."""
    pass


def test_read_answers_admin_edit():
    """Edit a ReadAnswer as admin."""
    pass


def test_read_answers_notowner_edit():
    """Edit a ReadAnswer not as admin or owner fails."""
    pass


def test_read_answers_admin_accept():
    """ConfirmReadAnswer accepted by admin."""
    pass


def test_read_answers_notadmin_accept():
    """ConfirmReadAnswer accepted by non admin fails."""
    pass


def test_read_answers_admin_accept_fails_accepted():
    """Accepting a ConfirmReadAnswer by an admin already accepted fails."""
    pass
