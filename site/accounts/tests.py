from django.test import TestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.text import slugify
from common.mixins import TestMixin
from .hashers import DrupalPasswordHasher
from .models import UserCustom
from .factories import UserFactory


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
    def test_get_absolute_url(self):
        """Should link to the user's profile page."""
        user = UserFactory()
        self.assertEqual(
            user.get_absolute_url(),
            reverse("profile", args=[user.slug]),
        )

    def test_get_name_returns_name_if_exists(self):
        """Should return `name` if it isn't blank."""
        user = UserFactory(name="Bob Bobbington")
        self.assertEqual(user.get_name(), user.name)

    def test_get_name_returns_username_if_full_name_not_exist(self):
        """Should return `username` if `name` is blank."""
        user = UserFactory(username="bob68")
        self.assertEqual(user.get_name(), user.username)

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

    def test_slug_created_from_username(self):
        """Should create a slug from the username when creating a user."""
        user = UserFactory()
        self.assertEqual(user.slug, slugify(user.username))

    def test_creates_unique_slugs(self):
        """Should create unique slugs even if usernames match."""
        user_a = UserFactory(username="test")
        user_b = UserFactory(username="te@st")
        self.assertNotEqual(user_a.slug, user_b.slug)


class ProfileDetailTest(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        user = UserFactory()
        self.assertLoginRequired(reverse("profile", args=[user.slug]))
