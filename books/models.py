"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from authentication.models import Author
from bookworm.mixins import (
    PublishableModelMixin,
    ProfileReferredMixin,
    PreserveModelMixin,
)
from meta_info.models import MetaInfo
from meta_info.models_localisation import LocaliseTag
from books.models_read import Thrill
from books.serializers_publish import (
    PublishBookSerializer,
    PublishReadingListSerializer,
    PublishBookReviewSerializer,
)


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
        max_length=16,
        db_index=True,
        blank=True,
    )
    ean = models.CharField(
        verbose_name=_('International Article Number'),
        max_length=16,
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
        PublishableModelMixin,
        PublicationMixin,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Books model."""

    id = HashidAutoField(
        primary_key=True,
        salt='p^oE*^4(%7;Yb:p_5Nuccz3-H?>wYJ4c',
    )
    author = models.ForeignKey(
        Author,
        related_name='books',
        verbose_name=_('Author'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    thrills = models.ManyToManyField(
        Thrill,
        related_name='books',
        verbose_name=_('Thrills'),
        blank=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='books+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Publishable:
        publishable_verification = None
        publishable_children = (
            'reviews',
        )
        serializer = PublishBookSerializer

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
        salt='KTEVvV\'e#Z*mO;d\';e1I.5T]aVwUZN"1',
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
        salt='oJI94-Ej+ylQ.lqxRIc`Y5!2_{_Q=zGh',
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
    # TODO: For screen reading ensure the file being read is recorded.
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
        PublishableModelMixin,
        ProfileReferredMixin,
        PreserveModelMixin,
):
    """Reading list model."""

    id = HashidAutoField(
        primary_key=True,
        salt='cF6/9w*hf.1xWzqmleOlY}>,!iWl;2@i',
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
    thrills = models.ManyToManyField(
        Thrill,
        related_name='reading_lists',
        verbose_name=_('Thrills'),
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

    class Publishable:
        publishable_verification = None
        publishable_children = None
        serializer = PublishReadingListSerializer

    class Meta:
        verbose_name = 'Reading List'
        verbose_name_plural = 'Reading Lists'

    @property
    def count(self):
        return self.books.all().count()

    def __str__(self):
        plural = 's' if len(self.books) > 1 else ''
        return f'{self.title} ({self.count} book{plural})'


class BookReview(
        PublishableModelMixin,
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
        salt='p6|v5qADW64CC<-4gMTnFh/N7.sV,wPG',
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
    progress = models.ForeignKey(
        BookProgress,
        related_name='reviewed_at',
        verbose_name=_('Progress'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    thrills = models.ManyToManyField(
        Thrill,
        related_name='reviews',
        verbose_name=_('Thrills'),
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

    class Publishable:
        publishable_verification = None
        publishable_children = None
        serializer = PublishBookReviewSerializer

    class Meta:
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'

    def __str__(self):
        return f'{self.book.title} reviewed by {self.profile.display_name}'
