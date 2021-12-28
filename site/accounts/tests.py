from django.contrib.auth import authenticate
from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from common.mixins import TestMixin
from common.test_utils import test_image
from uniforms.factories import JacketUserFactory

from .factories import UserFactory
from .models import UserCustom


class UserCustomTest(TestMixin, TestCase):
    def test_get_absolute_url(self):
        """Should link to the user's profile page."""
        user = UserFactory()
        self.assertEqual(
            user.get_absolute_url(),
            reverse("accounts:ProfileDetail", args=[user.slug]),
        )

    def test_to_str_name_exists(self):
        """`__str__` should return name when it exists."""
        user = UserFactory(name="Bob Bobbington")
        self.assertEqual(str(user), user.name)

    def test_to_str_name_not_exist(self):
        """`__str__` should return username when name doesn't exist."""
        user = UserFactory(name="")
        self.assertEqual(str(user), user.username)

    def test_get_name_returns_name_if_exists(self):
        """Should return `name` if it exists."""
        user = UserFactory(name="Bob Bobbington")
        self.assertEqual(user.get_name(), user.name)

    def test_get_name_returns_username_if_name_not_exist(self):
        """Should return `username` if `name` doesn't exist."""
        user = UserFactory(name="")
        self.assertEqual(user.get_name(), user.username)

    def test_default_membership_status_is_active(self):
        """The default membership status should be `ACTIVE`."""
        user = UserFactory()
        self.assertEqual(user.membership_status, UserCustom.MembershipStatus.ACTIVE)

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

    def test_get_avatar_url_avatar_exists(self):
        """
        `get_avatar_url` should return the URL to
        the user's avatar when it exists.
        """
        user = UserFactory(avatar=test_image())
        self.assertEqual(user.get_avatar_url(), user.avatar.url)

    def test_get_avatar_url_avatar_not_exist(self):
        """
        `get_avatar_url` should return the default avatar
        when the user's avatar doesn't exist.
        """
        user = UserFactory()
        self.assertEqual(user.get_avatar_url(), static("accounts/default-avatar.svg"))

    def test_get_jacket(self):
        user = UserFactory()
        jacket_user = JacketUserFactory(user=user)
        self.assertEqual(user.get_jacket(), jacket_user.jacket)

    def test_get_jacket_not_exist(self):
        user = UserFactory()
        self.assertIsNone(user.get_jacket())


class ProfileDetailTest(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        user = UserFactory()
        self.assertLoginRequired(reverse("accounts:ProfileDetail", args=[user.slug]))
