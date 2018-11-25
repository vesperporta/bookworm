"""BookReview End to End tests."""

from faker import Faker

fake = Faker()


def test_book_review_create():
    """Anyone can create a BookReview."""
    pass


def test_book_review_owner_edit():
    """Owner can edit a BookReview."""
    pass


def test_book_review_admin_edit():
    """Admin can edit a BookReview."""
    pass


def test_book_review_notowner_edit():
    """Non owner fails editing a BookReview."""
    pass


def test_book_review_search():
    """Anyone can search a BookReview."""
    pass
