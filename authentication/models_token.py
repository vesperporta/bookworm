"""Tokenisation of objects for simple authentication."""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from hashid_field import HashidAutoField

from bookworm.mixins import PreserveModelMixin


class TokenManager(models.Manager):

    def get_cipher(self):
        """Create AES cipher to manage the storage of values.

        @:return Crypto.cipher.AES
        """
        return AES.new(
            settings.AES_KEY_AUTHENTICATION,
            AES.MODE_CBC,
            settings.AES_IV456_AUTHENTICATION,
        )

    def generate_sha256(self, seed=None):
        """Generate a random hexadecimal str, 2 salts are used.

        @:param seed: str to set for hashing or now timestamp is used.

        @:return str
        """
        sha_hash = SHA256.new()
        if not seed:
            seed = str(timezone.now().timestamp())
        sha_hash.update(
            f'{settings.TOKEN_SALT_START}{seed}{settings.TOKEN_SALT_END}'
        )
        return sha_hash.hexdigest()

    def create_token(
            self, token_key, token_value=None, expiry=None, single_use=True):
        """Create a token.

        @:param token_key: str the key to identify this Token by.
        @:param token_value: str optional value to store as validation value.
        @:param expiry: datetime the token will expire.
        @:param single_use: bool determines a one off use.

        @:return Token
        """
        expire_in_day = timezone.now() + timedelta(days=1)
        expiry_expected = expiry if expiry else expire_in_day
        aes_object = TokenManager.get_cipher()
        if not token_value:
            token_value = TokenManager.generate_sha256(token_key)
        cipher_text = aes_object.encrypt(token_value)
        self.filter(
            key=token_key,
            validated=False,
        ).delete()
        return Token.objects.create(
            key=token_key,
            value=cipher_text,
            expiry=expiry_expected,
            single_use=single_use,
        )

    def validation(self, token_key, token_value):
        """Validate a key value pair.

        @:param token_key: str identifier.
        @:param token_value: str value stored in cipher.

        @:return bool
        """
        token = Token.objects.filter(key=token_key).first()
        return token.validate(token_value)


class Token(PreserveModelMixin):
    """Simple token object."""

    id = HashidAutoField(
        primary_key=True,
        salt=settings.SALT_AUTHENTICATION_CONTACTMETHOD,
    )
    key = models.TextField(
        verbose_name=_('Token key'),
    )
    value = models.TextField(
        verbose_name=_('Token value'),
        blank=True,
    )
    single_use = models.BooleanField(
        verbose_name=_('Single validation use'),
        default=True,
    )
    validated = models.BooleanField(
        verbose_name=_('Confirmation of validation'),
        default=False,
    )
    expiry = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    objects = TokenManager()

    def validate(self, expected_value):
        """Validate the stored value against an expected.

        @:param expected_value: str value expected to match.

        @:return bool
        """
        if not self.value:
            return False
        now = timezone.now()
        expired = self.expiry < now
        aes_object = self.objects.get_cipher()
        is_valid = aes_object.decrypt(self.value) == expected_value
        if expired or is_valid:
            self.validated = True
            self.expiry = now
            self.save()
        if expired or self.single_use:
            self.delete()
        if expired:
            return False
        return is_valid
