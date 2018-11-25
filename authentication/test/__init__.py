"""Authentication test factories."""

import datetime
import pytz
import factory
from factory.django import DjangoModelFactory

from django.db.models.signals import (
    pre_save,
    post_save,
    post_delete,
)

from django_common.auth_backends import User
from factory.fuzzy import FuzzyChoice
from faker.utils.text import slugify

from authentication.models import Profile, PersonMixin, ContactMethod
from meta_info.models import MetaInfo, HashedTag, Tag


_start_date = datetime.datetime(2018, 1, 1, tzinfo=pytz.UTC)

@factory.django.mute_signals(pre_save, post_save, post_delete)
class TagFactory(DjangoModelFactory):
    """Factory for tag."""

    copy = factory.fuzzy.FuzzyText(length=8)

    @factory.post_generation
    def slug(self, create, extracted, **kwargs):
        """Slugs are derived from the copy supplied."""
        if create and extracted:
            self.slug = slugify(self.copy)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """By default there are no Tags supplied."""
        if not create:
            return
        if extracted:
            for contact in extracted:
                self.contacts.add(contact)

    class Meta:
        model = Tag


@factory.django.mute_signals(pre_save, post_save, post_delete)
class HashedTagFactory(DjangoModelFactory):
    """Factory for hashed_tag."""

    slug = factory.fuzzy.FuzzyText(length=8)
    copy = factory.fuzzy.FuzzyText(length=8)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """By default there are no Tags supplied."""
        if not create:
            return
        if extracted:
            for contact in extracted:
                self.contacts.add(contact)

    class Meta:
        model = HashedTag


@factory.django.mute_signals(pre_save, post_save, post_delete)
class MetaInfoFactory(DjangoModelFactory):
    """Factory for meta_info."""

    copy = '{}'
    json = {}
    uri = ''

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """By default there are no Tags supplied."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.contacts.add(tag)

    @factory.post_generation
    def chain(self, create, extracted, **kwargs):
        """By default there is no chain supplied."""
        if not create:
            return
        if extracted:
            for meta_tag in extracted:
                self.contacts.add(meta_tag)

    class Meta:
        model = MetaInfo


@factory.django.mute_signals(pre_save, post_save, post_delete)
class ContactMethodFactory(DjangoModelFactory):
    """Factory for contact methods."""

    type = FuzzyChoice((t[0] for t in ContactMethod.TYPES))
    detail = factory.Faker('email')
    email = factory.Faker('email')
    uri = factory.Faker('url')

    @factory.post_generation
    def meta_info(self, create, extracted, **kwargs):
        """MetaInfo object creation for model."""
        if create and extracted:
            self.meta_info = MetaInfoFactory()

    class Meta:
        model = ContactMethod


@factory.django.mute_signals(pre_save, post_save, post_delete)
class ProfileFactory(DjangoModelFactory):
    """Factory for profiles."""

    email = factory.Faker('email')
    name_title = FuzzyChoice((t[0] for t in PersonMixin.NAME_TITLES))
    name_first = factory.Faker('first_name')
    name_family = factory.Faker('last_name')
    name_middle = factory.Faker('first_name')
    name_display = factory.Faker('first_name')
    birth_date = factory.Faker('date_object')
    death_date = factory.Faker('date_object')

    @factory.post_generation
    def meta_info(self, create, extracted, **kwargs):
        """MetaInfo object creation for model."""
        if create and extracted:
            self.meta_info = MetaInfoFactory()

    @factory.post_generation
    def contacts(self, create, extracted, **kwargs):
        """Create ContactMethods when they are requested."""
        if not create:
            return
        if extracted:
            for contact in extracted:
                self.contacts.add(contact)

    class Meta:
        model = Profile


@factory.django.mute_signals(pre_save, post_save, post_delete)
class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('user_name')
    is_superuser = False
    profile = factory.RelatedFactory(ProfileFactory, 'user')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_staff = False
    is_active = True
    date_joined = factory.fuzzy.FuzzyDateTime(_start_date)
    last_login = factory.fuzzy.FuzzyDateTime(_start_date)

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Hash passed password and store."""
        if create and extracted:
            self.set_password(extracted)
            self.save()

    class Meta:
        model = User
