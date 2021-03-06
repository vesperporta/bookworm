"""Profile models."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_common.auth_backends import User

from model_utils import Choices
from hashid_field import HashidAutoField

from authentication.models_token import Token
from bookworm.mixins import PreserveModelMixin
from file_store.models import Imagable
from meta_info.models import MetaInfo, MetaInfoMixin
from posts.models import Emotable

SOCIAL_PLATFORMS = (
    ('Facebook', ('social', ), ),
    ('Twitter', ('social', ), ),
    ('Google', ('social', ), ),
    ('Instagram', ('social', ), ),
    ('Pintrest', ('social', ), ),
)
TAGS = (
    'primary',
    'billing',
    'email',
    'mobile',
    'landline',
    'postal',
    'social',
) + SOCIAL_PLATFORMS


class ContactMethod(PreserveModelMixin):
    """Contact method."""

    TYPES = Choices(
        (0, 'email', _('Email')),
        (1, 'mobile', _('Mobile Number')),
        (2, 'landline', _('Landline Number')),
        (3, 'postal', _('Postal Address')),
        (4, 'billing', _('Billing Address')),
        (5, 'social', _('Social Network ID')),
    )

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_CONTACTMETHOD,
    )
    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.email,
        blank=True,
    )
    detail = models.TextField(
        db_index=True,
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        blank=True,
        null=True,
    )
    uri = models.URLField(
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='contacts+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Contact Method'
        verbose_name_plural = 'Contact Methods'

    def __str__(self):
        """Valid email output of profile."""
        contact_type = self.TYPES[self.type]
        return f'ContactMethod({self.id} - {contact_type} {self.detail})'


class PersonMixin(models.Model):
    """Person mixin."""

    NAME_TITLES = Choices(
        (0, 'mrs', _('Mrs')),
        (1, 'mr', _('Mr')),
        (2, 'miss', _('Miss')),
        (3, 'ms', _('Ms')),
        (4, 'dr', _('Dr')),
        (5, 'sir', _('Sir')),
    )

    name_title = models.IntegerField(
        choices=NAME_TITLES,
        blank=True,
        null=True,
    )
    name_first = models.CharField(
        max_length=64,
        db_index=True,
        blank=True,
        null=True,
    )
    name_family = models.CharField(
        max_length=64,
        db_index=True,
        blank=True,
        null=True,
    )
    name_middle = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    name_display = models.CharField(
        max_length=254,
        db_index=True,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
    )
    death_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def display_name(self):
        """Generate the profiles display name when none is provided."""
        name_list = ['name_first', 'name_family', ]
        return self.name_display or \
            ' '.join([getattr(self, n) for n in name_list if getattr(self, n)])

    @property
    def name_concat(self):
        """Create a synthetic concatenation of the name provided.."""
        name_list = ['name_first', 'name_family', ]
        name = ' '.join(
            [getattr(self, n) for n in name_list if getattr(self, n)]
        )
        if self.name_title:
            title = self.NAME_TITLES[self.name_title]
            name = f'{title} {name}'
        return name


class Profile(Imagable, PersonMixin, PreserveModelMixin):
    """Profile model."""

    TYPES = Choices(
        (0, 'user', _('User')),
        (1, 'elevated', _('Elevated')),
        (2, 'admin', _('Administrator')),
        (3, 'destroyer', _('Destroyer of Worlds')),
    )

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_PROFILE,
    )
    user = models.OneToOneField(
        User,
        related_name='profile',
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    type = models.IntegerField(
        choices=TYPES,
        default=TYPES.user,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
        unique=True,
    )
    contacts = models.ManyToManyField(
        ContactMethod,
        related_name='profiles+',
        verbose_name=_('Contact Methods'),
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='profiles+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    auth_token = models.ForeignKey(
        Token,
        related_name='authentication_token+',
        verbose_name=_('Authentication'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Valid email output of profile."""
        return f'Profile({self.id} - {self.display_name} "{self.email}")'


class Author(Emotable, Imagable, PersonMixin, PreserveModelMixin):
    """Author model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_AUTHOR,
    )
    contacts = models.ManyToManyField(
        ContactMethod,
        related_name='authors+',
        verbose_name=_('Contact Methods'),
    )
    profile = models.ForeignKey(
        Profile,
        related_name='pen_names',
        verbose_name=_('Profile'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    meta_info = models.ForeignKey(
        MetaInfo,
        related_name='authors+',
        verbose_name=_('Meta data'),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        """Valid email output of profile."""
        return f'Author({self.id} "{self.display_name}")'


class ProfileSetting(PreserveModelMixin, MetaInfoMixin):
    """Profile Settings model."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_PROFILESETTING,
    )
    profile = models.ForeignKey(
        Profile,
        related_name='settings',
        verbose_name=_('Profile'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'Profile Setting'
        verbose_name_plural = 'Profile Settings'
