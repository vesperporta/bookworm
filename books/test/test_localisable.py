"""Images End to End tests."""

from faker import Faker

fake = Faker()


def test_book_localised():
    """Fetch a Books details localised according to a localisation code."""
    pass


def test_book_localised_no_code():
    """Localisation code is required."""
    pass


def test_book_localised_unknown_code():
    """Unknown codes return an error."""
    pass
