"""Books models."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from hashid_field import HashidAutoField

from bookworm.mixins import (ProfileReferredMixin, PreserveModelMixin)
from books.models import (Book, BookChapter)


class Thrill(
        PreserveModelMixin,
        ProfileReferredMixin,
):
    """Thrill model."""

    PREFIX = '👓'  # 👓 = Thrill

    id = HashidAutoField(
        primary_key=True,
        salt='FpbU^<z(tC9ax(e"lkca9a(z0rv-+Y[P',
    )
    book = models.ForeignKey(
        Book,
        related_name='thrills',
        verbose_name=_('Book'),
        on_delete=models.DO_NOTHING,
        blank=True,
    )

    class Meta:
        verbose_name = 'Thrill'
        verbose_name_plural = 'Thrills'

    # def save(self):
    #     return super().save()

    def __str__(self):
        """Display only as URI valid slug."""
        return '{}{} "{}"'.format(
            self.PREFIX,
            self.profile,
            self.book,
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

    id = HashidAutoField(
        primary_key=True,
        salt='L>fZ(XHL?!do[BlbGFIdA99fzkY;k!=+',
    )
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
        null=True,
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

    id = HashidAutoField(
        primary_key=True,
        salt='JBKvt+AzL@mRF*^zw.9U$5;pnTFl[665',
    )
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

    id = HashidAutoField(
        primary_key=True,
        salt='M&!_eO>;`ZIO&nnUHH*,*-#3:P&0KD]$',
    )
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
