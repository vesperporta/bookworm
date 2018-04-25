"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.exceptions import DataMissingIntegrityError
from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import (Book, ReadingList, BookChapter)


class Thrill(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Want model."""

    PREFIX = '👓'  # 👓 = Thrill

    id = HashidAutoField(primary_key=True)
    book = models.ForeignKey(
        Book,
        related_name='thrills',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    reading_list = models.ForeignKey(
        ReadingList,
        related_name='thrills',
        verbose_name=_('Reading List'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Thrill'
        verbose_name_plural = 'Thrills'

    def save(self):
        if (not self.book and not self.reading_list) or \
                (self.book and self.reading_list):
            raise DataMissingIntegrityError(self, 'book', 'reading_list')
        return super().save()

    def __str__(self):
        """Display only as URI valid slug."""
        return '{}{} "{}"'.format(
            self.PREFIX,
            self.profile,
            self.book if self.book else self.reading_list,
        )


class ConfirmReadQuestion(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """ConfirmRead model."""

    DIFFICULTIES = Choices(
        (0, 'basic', _('Basic: Read the title.')),
        (1, 'simple', _('Simple: Highlight question.')),
        (2, 'normal', _('Normal: Read the book.')),
        (3, 'hard', _('Hard: Full on factual.')),
        (4, 'transcend', _('Transcend: 🖖')),
    )

    id = HashidAutoField(primary_key=True)
    difficulty = models.IntegerField(
        choices=DIFFICULTIES,
        default=DIFFICULTIES.simple,
        blank=True,
    )
    book = models.ForeignKey(
        Book,
        related_name='confirm_read+',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    chapter = models.ForeignKey(
        BookChapter,
        related_name='confirm_read+',
        verbose_name=_('Chapter'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    question = models.CharField(
        verbose_name=_('Question'),
        max_length=400,
    )

    class Meta:
        verbose_name = 'Confirm Read Question'
        verbose_name_plural = 'Confirm Read Questions'

    def __str__(self):
        """Display only as URI valid slug."""
        return '{} "{}"'.format(self.book, self.question)


class ConfirmReadAnswer(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Defines answers for read question."""

    id = HashidAutoField(primary_key=True)
    question = models.ForeignKey(
        ConfirmReadQuestion,
        related_name='answers',
        verbose_name=_('Question'),
        on_delete=models.DO_NOTHING,
    )
    answer = models.BooleanField(
        verbose_name=_('Is Answer'),
        default=False,
    )
    copy = models.CharField(
        verbose_name=_('Answer Copy'),
        max_length=400,
    )

    class Meta:
        verbose_name = 'Confirm Read Answer'
        verbose_name_plural = 'Confirm Read Answers'

    def __str__(self):
        """Display only as URI valid slug."""
        return '{} "{}"{}'.format(
            self.question.id,
            self.copy[:30],
            '👍' if self.answer else '👎',
        )


class Read(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Read model."""

    PREFIX = '📖'  # 📖 = Read

    id = HashidAutoField(primary_key=True)
    book = models.ForeignKey(
        Book,
        related_name='read',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )
    question = models.ForeignKey(
        ConfirmReadQuestion,
        related_name='read',
        verbose_name=_('Question Challenge'),
        on_delete=models.DO_NOTHING,
    )
    answer = models.ForeignKey(
        ConfirmReadAnswer,
        related_name='read_selected',
        verbose_name=_('Challenge Answer'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    class Meta:
        verbose_name = 'Read'
        verbose_name_plural = 'Read'

    @property
    def answered_correctly(self):
        return self.question.answers.filter(answer=True).first() is self.answer

    def __str__(self):
        """Display only as URI valid slug."""
        return '{}{} "{}"'.format(self.PREFIX, self.profile, self.book)
