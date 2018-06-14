"""Books models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from authentication.models import Author
from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from meta_info.models import MetaInfo
from meta_info.models_localisation import LocaliseTag
from posts.models import Emotable


GENRES = (
    ('Action', ('Genre',), ),
    ('Adventure', ('Genre',), ),
    ('Romance', ('Genre',), ),
    ('Fiction', ('Genre',), ),
    ('Fantasy', ('Genre',), ),
    ('Non Fiction', ('Genre',), ),
    ('Science Fiction', ('Genre',), ),
    ('Satire', ('Genre',), ),
    ('Drama', ('Genre',), ),
    ('Mystery', ('Genre',), ),
    ('Poetry', ('Genre',), ),
    ('Comics', ('Genre',), ),
    ('Horror', ('Genre',), ),
    ('Art', ('Genre',), ),
    ('Diaries', ('Genre',), ),
    ('Guide', ('Genre',), ),
    ('Travel', ('Genre',), ),
)
TAGS = (
    'Genre',
    'Author',
    'Publisher',
    'Collaborator',
    'Collaborators',
    'Distributor',
    'Published Date',
    'Publication Issue',
) + GENRES


class PublicationMixin(models.Model):
    """Publication mixin."""

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=200,
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    isbn = models.CharField(
        verbose_name=_('International Standard Book Number'),
        max_length=10,
        blank=True,
    )
    ean = models.CharField(
        verbose_name=_('International Article Number'),
        max_length=13,
        db_index=True,
        blank=True,
    )
    localisations = models.ManyToManyField(
        LocaliseTag,
        related_name='publications+',
        verbose_name=_('Localised Copy'),
        blank=True,
    )

    class Meta:
        abstract = True


class Book(
        Emotable,
        PublicationMixin,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Books model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_BOOK,
    )
    author = models.ForeignKey(
        Author,
        related_name='books',
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='books+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        """Title and author of book."""
        author = self.author.display_name if self.author else 'Unknown'
        return f'{self.title} by {author}'


class BookProgress(
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Book progress model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_BOOKPROGRESS,
    )
    percent = models.FloatField()
    page = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    start = models.BigIntegerField()
    end = models.BigIntegerField(
        blank=True,
        null=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='progress+',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )
    # TODO: For screen reading ensure the file being read is recorded.

    class Meta:
        verbose_name = 'Progress'
        verbose_name_plural = 'Progresses'

    def __str__(self):
        """Title and percent of book progress."""
        return f'{self.book.title} at {self.percent}%'


class BookChapter(PreserveModelMixin):
    """Book chapter model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_BOOKCHAPTER,
    )
    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    progress = models.ForeignKey(
        BookProgress,
        related_name='chapter_progress+',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='chapters',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )
    localisations = models.ManyToManyField(
        LocaliseTag,
        related_name='publication_chapters+',
        verbose_name=_('Localised Copy'),
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='book_chapters+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Book Chapter'
        verbose_name_plural = 'Book Chapters'

    def __str__(self):
        return f'{self.book.title} Chapter: {self.title}'


class ReadingList(
        Emotable,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Reading list model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_READINGLIST,
    )
    title = models.CharField(
        max_length=200,
        db_index=True,
    )
    books = models.ManyToManyField(
        Book,
        related_name='reading_lists',
        verbose_name=_('Books'),
    )
    localisations = models.ManyToManyField(
        LocaliseTag,
        related_name='reading_lists+',
        verbose_name=_('Localised Copy'),
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='reading_lists+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Reading List'
        verbose_name_plural = 'Reading Lists'

    @property
    def count(self):
        return self.books.all().count()

    def add_book(self, book):
        book = book if type(book) is Book else Book.objects.get(id=book)
        self.books.add(book)

    def remove_book(self, book):
        book = book if type(book) is Book else Book.objects.get(id=book)
        self.books.remove(book)

    def __str__(self):
        plural = 's' if len(self.books.all()) > 1 else ''
        return f'{self.title} ({self.count} book{plural})'


class BookReview(
        Emotable,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Book reviews model."""

    TYPES = Choices(
        (0, 'review', _('Review')),
        (1, 'footnote', _('Footnote')),
        (2, 'margin', _('Margin note')),
        (3, 'line', _('Line highlight')),
        (4, 'paragraph', _('Paragraph highlight')),
    )

    RATINGS = Choices(
        (0, 'unrated', _('Unrated')),
        (1, 'terrible', _('Terrible and Trashy')),
        (2, 'junk', _('Junk Pile')),
        (3, 'ok', _('Readable')),
        (4, 'good', _('Good Read')),
        (5, 'brilliant', _('Couldn\'t Put Down')),
    )

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_BOOKREVIEW,
    )
    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.review,
        blank=True,
    )
    copy = models.TextField(
        db_index=True,
    )
    rating = models.IntegerField(
        choices=RATINGS,
        default=RATINGS.unrated,
        blank=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='reviews',
        verbose_name=_('Book'),
        on_delete=models.PROTECT,
    )
    infered_progress = models.ForeignKey(
        BookProgress,
        related_name='infered_reviewed_at+',
        verbose_name=_('Infered Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    progress = models.ForeignKey(
        BookProgress,
        related_name='reviewed_at',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    localisations = models.ManyToManyField(
        LocaliseTag,
        related_name='publication_reviews+',
        verbose_name=_('Localised Copy'),
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='book_reviews+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'

    def __str__(self):
        return f'{self.book.title} reviewed by {self.profile.display_name}'
