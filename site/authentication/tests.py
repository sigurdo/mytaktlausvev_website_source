from django.test import TestCase

from .hashers import DrupalPasswordHasher


class DrupalPasswordHasherTest(TestCase):
    def test_works_with_newer_drupal_password_hashes(self):
        """Should work with newer, Drupal 7+ password hashes."""
        password = "DifficultPassword123"
        encoded = "drupal$$S$5FIcboyzv1ZD/OZDb4w/4HSlnsPlwbr/PWLWrHPWrJp8eXOQQaWJ"
        hasher = DrupalPasswordHasher()
        self.assertTrue(hasher.verify(password, encoded))

    def test_works_with_updated_drupal_password_hashes(self):
        """Should work with password hashes updated in Drupal's `user_update_7000()`"""
        password = "SimpleEasyPassword"
        encoded = "drupal$U$S$5I5Ht7YwxFRiMiJhBjyt42Ji2WRndX2dCx1jyktH92PeQp0xWdgi"
        hasher = DrupalPasswordHasher()
        self.assertTrue(hasher.verify(password, encoded))
