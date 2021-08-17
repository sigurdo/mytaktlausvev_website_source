from django.test import TestCase
from django.contrib.auth import authenticate
from .hashers import DrupalPasswordHasher
from .models import UserCustom


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


class UserCustomTest(TestCase):
    def test_can_login_with_newer_drupal_password_hashes(self):
        """Should be able to login with newer, Drupal 7+ password hashes."""
        password = "DifficultPassword123"
        encoded = "drupal$$S$5FIcboyzv1ZD/OZDb4w/4HSlnsPlwbr/PWLWrHPWrJp8eXOQQaWJ"
        UserCustom.objects.create(username="Bob", password=encoded)
        self.assertIsNotNone(authenticate(username="Bob", password=password))

    def test_can_login_with_updated_drupal_password_hashes(self):
        """Should be able to login with password hashes updated in Drupal's `user_update_7000()`"""
        password = "SimpleEasyPassword"
        encoded = "drupal$U$S$5I5Ht7YwxFRiMiJhBjyt42Ji2WRndX2dCx1jyktH92PeQp0xWdgi"
        UserCustom.objects.create(username="Bob", password=encoded)
        self.assertIsNotNone(authenticate(username="Bob", password=password))

    def test_login_usernames_case_insensitive(self):
        """
        When logging in the username should be case insensitive.
        """
        password = "SuperSafePassword123"
        UserCustom.objects.create_user(username="Bob", password=password)
        self.assertIsNotNone(authenticate(username="Bob", password=password))
        self.assertIsNotNone(authenticate(username="BoB", password=password))
        self.assertIsNotNone(authenticate(username="bob", password=password))
        self.assertIsNotNone(authenticate(username="BOB", password=password))

    def test_creating_user_username_case_insensitive(self):
        """
        When creating a user the username should be case insensitive.
        """
        UserCustom.objects.create_user(username="BOB")
        with self.assertRaises(ValueError):
            UserCustom.objects.create_user(username="bob")
