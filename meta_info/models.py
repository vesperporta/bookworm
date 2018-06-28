"""Meta Information models."""

import hashlib

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from hashid_field import HashidAutoField

from bookworm.mixins import PreserveModelMixin


class TagMixin(models.Model):
    """Tagging base mixin."""

    slug = models.SlugField(
        db_index=True,
        unique=True,
        blank=True,
    )
    copy = models.CharField(
        max_length=200,
        db_index=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='tag_tags+',
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract = True


class TagManager(models.Manager):
    """Handle tags."""

    def get_or_create_tag(self, copy, tags=[]):
        """Manage the creation of Tag objects with respect to child tags.

        @param copy: Expected display name for a tag.
        @param tags: List or Tuple of strings for expected child tags.

        @return Tag object.
        """
        tag_rtn = self.filter(slug__iexact=slugify(copy)).first()
        if not tag_rtn:
            tag_rtn = self.create(copy=copy)
        if type(tags) is not list or type(tags) is not tuple:
            return tag_rtn
        tag_tags = list(tag_rtn.tags.all())
        for tag in tags:
            if type(tag) is str:
                sub_tag = self.create(copy=tag)
            elif type(tag) is TagMixin:
                sub_tag = tag
            if sub_tag:
                tag_tags.append(sub_tag)
            sub_tag = None
        if tag_tags:
            tag_rtn.tags.set(tag_tags)
            tag_rtn.save()
        return tag_rtn


class Tag(TagMixin, PreserveModelMixin):
    """Tag model."""

    PREFIX = '#'  # hash

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_TAG,
    )

    objects = TagManager()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Display only as URI valid slug."""
        return f'Tag({self.PREFIX}{self.copy})'


class HashedTag(TagMixin, PreserveModelMixin):
    """HashedTag model."""

    PREFIX = '#'  # hash

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_HASHEDTAG,
    )

    objects = TagManager()

    class Meta:
        verbose_name = 'HashedTag'
        verbose_name_plural = 'HashedTags'

    def save(self, *args, **kwargs):
        self.slug = hashlib.md5(str(self.copy).encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        """Display only as URI valid slug."""
        return f'HashedTag({self.PREFIX}{self.copy})'


class MetaInfoMixin(models.Model):
    """Meta mixin model."""

    copy = models.TextField(
        db_index=True,
        blank=True,
    )
    json = JSONField(
        default={},
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags+',
        verbose_name=_('Tags'),
        blank=True,
    )

    class Meta:
        abstract = True


class MetaInfo(MetaInfoMixin, PreserveModelMixin):
    """Meta model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_METAINFO_METAINFO,
    )
    uri = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
    )
    chain = models.ManyToManyField(
        'MetaInfo',
        verbose_name=_('Meta Data Chain'),
        blank=True,
    )

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'

    def __str__(self):
        """Represent MetaInfo in brevity from complex store."""
        description = self.copy if self.copy else self.uri
        if not self.copy:
            description = 'meta empty'
        return '{} "{}" tags:{}'.format(
            self.id,
            description[:20],
            self.tags.count()
        )
