"""Books models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from model_utils import Choices
from hashid_field import HashidAutoField

from books.exceptions import (
    AnswerAlreadyAcceptedValidation,
    CannotAcceptOwnAnswerValidation,
)
from books.tasks import answer_accepted_create_read
from bookworm.mixins import (
    ProfileReferredMixin,
    PreserveModelMixin,
)
from posts.models import Emotable, Post


class ConfirmReadQuestion(
        Emotable,
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
    multi_choice_answer = models.ForeignKey(
        'books.ConfirmReadQuestion',
        related_name='multi_choice',
        verbose_name=_('Answer'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
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
):
    """Defines answers for read question.

    To have publishable objcts copies of this object are expected.
    Each replication of the parent / root object is required to have a list
    of ReadingList, Profile ids, or key words defining pre-determined groups.
    Pre-determined groups: gloable, or noone.
    """

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
    is_true = models.NullBooleanField(
        verbose_name=_('Boolean Answer'),
        default=None,
        blank=True,
        null=True,
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
        return bool(self.accepted_by)

    def __str__(self):
        """Display only as URI valid slug."""
        answers = '👍' if self.correct else '👎'
        return f'{self.id} {answers} for question: {self.question.id}'

    def accept_answer(self, accepted_from):
        """Assign a Profile as the object accepting this answer."""
        if self.accepted_by:
            raise AnswerAlreadyAcceptedValidation(self.accepted_by)
        if accepted_from.id == self.profile.id:
            raise CannotAcceptOwnAnswerValidation()
        self.accepted_at = now()
        self.accepted_by = accepted_from
        self.save()
        answer_accepted_create_read(self)


class Read(Emotable, PreserveModelMixin, ProfileReferredMixin):
    """Read model.

    📖 = Read
    """

    PREFIX = '📖'

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
        return bool(self.answer.accepted_at)

    def __str__(self):
        """Display only as URI valid slug."""
        return f'{self.PREFIX}{self.profile.display_name} "{self.book.title}"'
