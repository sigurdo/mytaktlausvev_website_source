from http import HTTPStatus
from urllib.parse import urlencode

from django.contrib.auth import authenticate
from django.core import mail
from django.db import IntegrityError
from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now

from common.mixins import TestMixin
from common.test_utils import test_image
from instruments.factories import InstrumentTypeFactory

from .factories import SuperUserFactory, UserFactory
from .forms import ImageSharingConsentForm, UserCustomCreateForm
from .models import UserCustom


class UserCustomManagerTestCase(TestCase):
    def test_active_includes_only_paying_members_and_aspirants(self):
        aspirant = UserFactory(membership_status=UserCustom.MembershipStatus.ASPIRANT)
        paying = UserFactory(membership_status=UserCustom.MembershipStatus.PAYING)
        UserFactory(membership_status=UserCustom.MembershipStatus.RETIRED)
        UserFactory(membership_status=UserCustom.MembershipStatus.HONORARY)

        self.assertQuerysetEqual(
            UserCustom.objects.active(),
            [aspirant, paying],
            ordered=False,
        )


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

    def test_default_membership_status_is_aspirant(self):
        """The default membership status should be `ASPIRANT`."""
        user = UserFactory()
        self.assertEqual(user.membership_status, UserCustom.MembershipStatus.ASPIRANT)

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
        with self.assertRaises(IntegrityError):
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


    def test_light_mode_defaults_to_false(self):
        """`light_mode` should default to false."""
        user = UserFactory()
        self.assertFalse(user.light_mode)

    def test_image_sharing_consent_defaults_to_unknown(self):
        """`image_sharing_consent` should default to unknown."""
        user = UserFactory()
        self.assertEqual(
            user.image_sharing_consent, UserCustom.ImageSharingConsent.UNKNOWN
        )

    def test_is_active_member_returns_true_for_active_members(self):
        """
        `is_active_member` should return true for active members,
        meaning paying members and aspirants.
        """
        self.assertTrue(
            UserFactory(
                membership_status=UserCustom.MembershipStatus.ASPIRANT
            ).is_active_member()
        )
        self.assertTrue(
            UserFactory(
                membership_status=UserCustom.MembershipStatus.PAYING
            ).is_active_member()
        )

    def test_is_active_member_returns_false_for_not_active_members(self):
        """
        `is_active_member` should return false for members that aren't active,
        meaning all members except paying members and aspirants.
        """
        self.assertFalse(
            UserFactory(
                membership_status=UserCustom.MembershipStatus.HONORARY
            ).is_active_member()
        )
        self.assertFalse(
            UserFactory(
                membership_status=UserCustom.MembershipStatus.RETIRED
            ).is_active_member()
        )
        self.assertFalse(
            UserFactory(
                membership_status=UserCustom.MembershipStatus.INACTIVE
            ).is_active_member()
        )

    def test_has_storage_access_defaults_to_false(self):
        """`has_storage_access` should default to false."""
        user = UserFactory()
        self.assertFalse(user.has_storage_access)

    def calendar_feed_token_unique(self):
        user = UserFactory()
        with self.assertRaises(IntegrityError):
            UserFactory(calendar_feed_token=user.calendar_feed_token)

    def calendar_feed_start_date_default_none(self):
        user = UserFactory()
        self.assertIsNone(user.calendar_feed_start_date)


class UserCustomCreateFormTestSuite(TestCase):
    def test_all_fields_except_student_card_number_required(self):
        """Should require all fields except `student_card_number` and `no_storage_access`."""
        form = UserCustomCreateForm()
        form.fields.pop("student_card_number")
        form.fields.pop("no_storage_access")
        for field in form.fields.values():
            self.assertTrue(field.required)

    def test_validate_username_case_insensitively(self):
        """
        Should raise a validation error
        if a user with the same username, case-insensitive, exists.
        """
        UserFactory(username="Lintbot")
        form = UserCustomCreateForm({"username": "lintbot"})
        self.assertIn(
            "Det eksisterar allereie ein brukar med dette brukarnamnet.",
            form.errors["username"],
        )

    def test_require_no_storage_access_if_no_student_card_number(self):
        """
        Should require `no_storage_access`
        if no student card number is provided.
        """
        form = UserCustomCreateForm({"no_storage_access": False})
        self.assertIn(
            "Feltet er påkrevd om du ikkje legg inn studentkortnummer.",
            form.errors["no_storage_access"],
        )

    def test_no_storage_access_not_required_if_student_card_number(self):
        """
        Shouldn't require `no_storage_access`
        if a student card number is provided.
        """
        form = UserCustomCreateForm(
            {"no_storage_access": False, "student_card_number": "123"}
        )
        self.assertNotIn("no_storage_access", form.errors.keys())


class UserCustomCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.data_user = {
            "username": "Lintbot",
            "email": "lintbot@lint.police",
            "password1": "Formatters4Eva",
            "password2": "Formatters4Eva",
            "name": "Overlintkonstabel Lintbot",
            "phone_number": "1-800-FORMATTING-NEEDED",
            "birthdate": "2021-12-18",
            "address": "A server near you",
            "student_card_number": "6C696E74",
            "no_storage_access": True,
            "instrument_type": InstrumentTypeFactory().pk,
            "membership_period": "2022, Spring - ",
        }

    def get_url(self):
        return reverse("accounts:UserCustomCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission_for_creating_users(self):
        """Should require permission for creating users."""
        self.assertPermissionRequired(self.get_url(), "accounts.add_usercustom")

    def test_sends_mail_to_created_user(self):
        """Should send an email to the created user."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.data_user)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.data_user["email"]])


class UserCustomUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.user = UserFactory()

    def get_url(self):
        return reverse("accounts:UserCustomUpdate", args=[self.user.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to edit users."""
        self.assertPermissionRequired(self.get_url(), "accounts.change_usercustom")

    def test_succeeds_if_self(self):
        """Should succeed if a user tries to edit their own account."""
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ProfileDetailTest(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        user = UserFactory()
        self.assertLoginRequired(reverse("accounts:ProfileDetail", args=[user.slug]))


class BirthdayListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("accounts:BirthdayList")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_includes_active_user_with_birthdate(self):
        """Should include active users with a birthdate."""
        user = UserFactory(
            membership_status=UserCustom.MembershipStatus.PAYING, birthdate=now()
        )

        self.client.force_login(user)
        response = self.client.get(self.get_url())

        self.assertIn(user, response.context["users"])

    def test_excludes_not_active_users(self):
        """Should exclude users that aren't active."""
        retired = UserFactory(
            membership_status=UserCustom.MembershipStatus.RETIRED, birthdate=now()
        )

        self.client.force_login(retired)
        response = self.client.get(self.get_url())

        self.assertNotIn(retired, response.context["users"])

    def test_excludes_users_without_birthdate(self):
        """Should exclude users that don't have a birthdate."""
        no_birthday = UserFactory(birthdate=None)

        self.client.force_login(no_birthday)
        response = self.client.get(self.get_url())

        self.assertNotIn(no_birthday, response.context["users"])


class ImageSharingConsentListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("accounts:ImageSharingConsentList")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission_for_viewing_consent(self):
        """Should require permission for viewing image sharing consent."""
        self.assertPermissionRequired(
            self.get_url(), "accounts.view_image_sharing_consent"
        )

    def test_includes_active_users_only(self):
        """Should include only active users."""
        active = UserFactory(membership_status=UserCustom.MembershipStatus.PAYING)
        retired = UserFactory(membership_status=UserCustom.MembershipStatus.RETIRED)

        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url())

        self.assertIn(active, response.context["users"])
        self.assertNotIn(retired, response.context["users"])


class ImageSharingConsentFormTestSuite(TestCase):
    def test_form_action_is_update_view_by_default(self):
        form = ImageSharingConsentForm()
        self.assertEqual(
            form.helper.form_action, reverse("accounts:ImageSharingConsentUpdate")
        )

    def test_form_action_includes_next_url_if_specified(self):
        next_url = reverse("dashboard:Dashboard")
        form = ImageSharingConsentForm(next_url)
        self.assertEqual(
            form.helper.form_action,
            f"{reverse('accounts:ImageSharingConsentUpdate')}?{urlencode({'next': next_url})}",
        )


class ImageSharingConsentUpdateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("accounts:ImageSharingConsentUpdate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_updates_image_sharing_consent(self):
        """Should update the image sharing consent of the current user."""
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {"image_sharing_consent": UserCustom.ImageSharingConsent.YES},
        )
        user.refresh_from_db()
        self.assertEqual(user.image_sharing_consent, UserCustom.ImageSharingConsent.YES)

    def test_redirects_to_profile_page_if_no_next_url(self):
        """Should redirect to the profile page if no next URL is specified."""
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(
            self.get_url(),
            {"image_sharing_consent": UserCustom.ImageSharingConsent.YES},
        )
        self.assertRedirects(response, user.get_absolute_url())

    def test_redirects_to_next_url_if_specified(self):
        """Should redirect to the next URL, if specified."""
        user = UserFactory()
        self.client.force_login(user)
        url = f"{self.get_url()}?{urlencode({'next': reverse('dashboard:Dashboard')})}"
        response = self.client.post(
            url, {"image_sharing_consent": UserCustom.ImageSharingConsent.YES}
        )
        self.assertRedirects(response, reverse("dashboard:Dashboard"))
