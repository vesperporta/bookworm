"""BookChapter End to End tests."""

from faker import Faker

fake = Faker()


def test_book_chapter_create():
    """Anyone can create a BookChapter."""
    pass


def test_book_chapter_elevated_edit():
    """Elevated Profile can edit a BookChapter."""
    pass


def test_book_chapter_admin_edit():
    """Admin Profile can edit a BookChapter."""
    pass


def test_book_chapter_notowner_edit():
    """Non Elevated Profile fails editing a BookChapter."""
    pass


def test_book_chapter_search():
    """Anyone can search a BookChapter."""
    pass
