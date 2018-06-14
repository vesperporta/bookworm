"""Books models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from posts.models import Emotable, Post
from books.policies import OwnerElevatedAndLockAccessMixin


class ConfirmReadQuestion(
        Emotable,
        PreserveModelMixin,
        ProfileReferredMixin,
        OwnerElevatedAndLockAccessMixin,
):
    """ConfirmRead model."""

    DIFFICULTIES = Choices(
        (0, 'basic', _('Basic: Read the title.')),
        (1, 'simple', _('Simple: Highlight question.')),
        (2, 'normal', _('Normal: Read the book.')),
        (3, 'hard', _('Hard: Full on factual.')),
        (4, 'transcend', _('Transcend: 🖖')),
    )

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_CONFIRMREADQUESTION,
    )
    difficulty = models.IntegerField(
        choices=DIFFICULTIES,
        default=DIFFICULTIES.simple,
        blank=True,
    )
    book = models.ForeignKey(
        'books.Book',
        related_name='confirm_read+',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )
    chapter = models.ForeignKey(
        'books.BookChapter',
        related_name='confirm_read+',
        verbose_name=_('Chapter'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    copy = models.CharField(
        verbose_name=_('Question'),
        max_length=400,
    )
    lock = models.BooleanField(
        verbose_name=_('Lock Changes'),
        blank=True,
        default=False,
    )

    class Meta:
        verbose_name = 'Confirm Read Question'
        verbose_name_plural = 'Confirm Read Questions'

    def __str__(self):
        """Display only as URI valid slug."""
        return f'{self.book} "{self.copy[:30]}" [{self.aggregation}]'


class ConfirmReadAnswer(
        PreserveModelMixin,
        ProfileReferredMixin,
        OwnerElevatedAndLockAccessMixin,
):
    """Defines answers for read question."""

    TYPES = Choices(
        (0, 'choice', _('Multiple choice answer to select from.')),
        (1, 'written', _('Written answer.')),
        (2, 'boolean', _('True or False.')),
    )
    TYPES_CHOICE = [TYPES.choice, TYPES.boolean, ]

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_CONFIRMREADANSWER,
    )
    question = models.ForeignKey(
        ConfirmReadQuestion,
        related_name='answers',
        verbose_name=_('Question'),
        on_delete=models.DO_NOTHING,
    )
    copy = models.CharField(
        verbose_name=_('Answer copy'),
        max_length=400,
    )
    lock = models.BooleanField(
        verbose_name=_('Lock Changes'),
        blank=True,
        default=False,
    )
    is_true = models.BooleanField(
        verbose_name=_('Boolean Answer'),
        blank=True,
        default=None,
    )
    is_answer = models.BooleanField(
        verbose_name=_('Is Answer for Multiple Choice'),
        default=False,
    )
    accepted_at = models.DateTimeField(
        verbose_name=_('Accepted When'),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        default=None,
    )
    accepted_by = models.ForeignKey(
        'authentication.Profile',
        verbose_name=_('Accepted By'),
        related_name='read_answers_accepted+',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Confirm Read Answer'
        verbose_name_plural = 'Confirm Read Answers'

    @property
    def correct(self):
        """Answer is correct."""
        return bool(self.is_answer or self.accepted_by)

    def __str__(self):
        """Display only as URI valid slug."""
        answers = '👍' if self.correct else '👎'
        return f'{self.id} {answers} for question: {self.question.id}'


class Read(
        Emotable,
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Read model."""

    PREFIX = '📖'  # 📖 = Read

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_BOOKS_READ,
    )
    book = models.ForeignKey(
        'books.Book',
        related_name='read',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
    )
    answer = models.ForeignKey(
        ConfirmReadAnswer,
        related_name='read_selected',
        verbose_name=_('Challenge Answer'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )
    post = models.ForeignKey(
        Post,
        related_name='read+',
        verbose_name=_('Comment Thread'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    class Meta:
        verbose_name = 'Read'
        verbose_name_plural = 'Read'

    @property
    def answered_correctly(self):
        """Read declaration is correct, answer given defines correctness."""
        return self.answer.correct

    def __str__(self):
        """Display only as URI valid slug."""
        return f'{self.PREFIX}{self.profile.display_name} "{self.book.title}"'
