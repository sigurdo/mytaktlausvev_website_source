# Snippet downloaded from https://djangosnippets.org/snippets/2924/
# License terms can be found at https://djangosnippets.org/about/tos/
# Snippet has been slightly modified.

from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import get_random_string
from collections import OrderedDict
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_noop as _
import hashlib


class DrupalPasswordHasherInvalidHashException(Exception):
    pass


class DrupalPasswordHasher(BasePasswordHasher):
    """
    Authenticate against Drupal 7 passwords.

    The passwords should be prefixed with drupal$ upon importing, such that
    Django recognizes them correctly. Drupal's method does some funny stuff
    (like truncating the hashed password), so you might not want to use this
    hasher for storing new passwords.
    """

    algorithm = "drupal"

    _DRUPAL_HASH_LENGTH = 55
    _DRUPAL_HASH_COUNT = 15

    _digests = {
        "$S$": hashlib.sha512,
        "$H$": hashlib.md5,
        "$P$": hashlib.md5,
    }

    _itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def _get_settings(self, encoded):
        settings_bin = encoded[:12]
        count_log2 = self._itoa64.index(settings_bin[3])
        count = 1 << count_log2
        salt = settings_bin[4:12]
        return {"count": count, "salt": salt}

    def _drupal_b64(self, input):
        output = ""
        count = len(input)
        i = 0
        while True:
            value = input[i]
            i += 1
            output += self._itoa64[value & 0x3F]
            if i < count:
                value |= input[i] << 8
            output += self._itoa64[(value >> 6) & 0x3F]
            i += 1
            if i >= count:
                break
            if i < count:
                value |= input[i] << 16
            output += self._itoa64[(value >> 12) & 0x3F]
            i += 1
            if i >= count:
                break
            output += self._itoa64[(value >> 18) & 0x3F]
        return output

    def _apply_hash(self, password, digest, settings):
        password = force_bytes(password)
        password_hash = digest(force_bytes(settings["salt"]) + password).digest()
        for _ in range(settings["count"]):
            password_hash = digest(password_hash + password).digest()
        return self._drupal_b64(password_hash)[: self._DRUPAL_HASH_LENGTH - 12]

    def salt(self):
        return get_random_string(8)

    def encode(self, password, salt):
        assert len(salt) == 8
        digest = "$S$"
        settings = {"count": 1 << self._DRUPAL_HASH_COUNT, "salt": salt}
        encoded_hash = self._apply_hash(password, self._digests[digest], settings)
        return (
            self.algorithm
            + "$"
            + digest
            + self._itoa64[self._DRUPAL_HASH_COUNT]
            + salt
            + encoded_hash
        )

    def verify(self, password, encoded):
        encoded = encoded.split("$", 1)[1]
        if encoded[0] == "U":
            # Imported passwords from old Drupal versions, see user_update_7000()
            encoded = encoded[1:]
            password = hashlib.md5(force_bytes(password)).hexdigest()
        digest = encoded[:3]
        if digest not in self._digests:
            raise DrupalPasswordHasherInvalidHashException()
        digest = self._digests[digest]
        settings = self._get_settings(encoded)

        encoded_hash = encoded[12:]
        password_hash = self._apply_hash(password, digest, settings)

        return password_hash == encoded_hash

    def safe_summary(self, encoded):
        encoded = encoded.split("$", 1)[1]
        settings = self._get_settings(encoded)
        return OrderedDict(
            [
                (_("algorithm"), self.algorithm),
                (_("iterations"), settings["count"]),
                (_("salt"), settings["salt"]),
                (_("hash"), encoded[12:]),
            ]
        )

    def must_update(self, encoded):
        encoded = encoded.split("$", 1)[1]
        if encoded[0] == "U":
            return True
        settings = self._get_settings(encoded)
        return settings["count"] < (1 << self._DRUPAL_HASH_COUNT)
