"""Emoting End to End tests."""

from faker import Faker

fake = Faker()


def test_book_emoted():
    """Create an Emote object for a Book."""
    pass


def test_book_emoted_already_emoted():
    """Emote on a Book the Profile has already emoted on fails response."""
    pass


def test_book_emoted_aggregation():
    """Create an Emote object for a Book ensure aggregation correct."""
    pass


def test_book_un_emote():
    """Remove an Emote from a Book."""
    pass


def test_book_un_emote_not_emoted():
    """Un-emote from a Book not emoted on fails."""
    pass
