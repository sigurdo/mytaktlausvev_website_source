from django.test import TestCase
from django.urls.base import reverse

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


class LoginViewTestSuite(TestCase):
    def get_url(self, next_url=""):
        return reverse("login") + f"?next={next_url}"

    def test_next_in_initial_form_data(self):
        """Should include `next` query param in initial form data."""
        next_url = "take-me-here"
        response = self.client.get(self.get_url(next_url))
        self.assertEqual(response.context["form"].initial["next"], next_url)
