"""Emoting End to End tests."""

from faker import Faker

fake = Faker()


def test_author_emoted():
    """Create an Emote object for an Author."""
    pass


def test_author_emoted_already_emoted():
    """Emote on an Author the Profile has already emoted on fails response."""
    pass


def test_author_emoted_aggregation():
    """Create an Emote object for an Author ensure aggregation correct."""
    pass


def test_author_un_emote():
    """Remove an Emote from an Author."""
    pass


def test_author_un_emote_not_emoted():
    """Un-emote from an Author not emoted on fails."""
    pass
