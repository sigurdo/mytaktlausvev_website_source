from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from accounts.models import UserCustom
from common.mixins import TestMixin
from common.utils import comma_seperate_list

from .factories import QuoteFactory
from .forms import QuoteForm


class QuoteTestSuite(TestMixin, TestCase):
    def test_to_str_quote_shorter_than_25_characters(self):
        """`__str__` should equal the quote, when it is shorter than 25 characters."""
        quote = QuoteFactory(quote="Du daua")
        self.assertEqual(
            str(quote),
            quote.quote,
        )

    def test_to_str_quote_longer_than_25_characters(self):
        """
        `__str__` should truncate the quote when it has more than 25 characters,
        and add an ellipsis.
        """
        quote = QuoteFactory(
            quote="Extremely long quote, spanning multiple lines, challenging the idea of what a quote really is."
        )
        self.assertEqual(str(quote), quote.quote[0:24] + "…")

    def test_quoted_as_or_users_is_quoted_as_if_it_exists(self):
        """`quoted_as_or_users` should equal `quoted_as` when it exists."""
        quote = QuoteFactory(quoted_as="Mørke Sjeler")
        self.assertEqual(quote.quoted_as_or_users(), quote.quoted_as)

        quote_with_user = QuoteFactory(quoted_as="Mørke Sjeler", users=[UserFactory()])
        self.assertEqual(
            quote_with_user.quoted_as_or_users(), quote_with_user.quoted_as
        )

    def test_quoted_as_or_users_is_users_if_no_quoted_as(self):
        """
        If the quote has no `quoted_as`,
        `quoted_as_or_users` should be `users` comma-separated.
        """
        user_1 = UserFactory()
        user_2 = UserFactory()
        quote = QuoteFactory(quoted_as="", users=[user_1, user_2])
        self.assertEqual(
            quote.quoted_as_or_users(),
            comma_seperate_list(
                [user_1.get_preferred_name(), user_2.get_preferred_name()]
            ),
        )


class QuoteFormTestSuite(TestMixin, TestCase):
    def test_inactive_users_not_in_users_queryset(self):
        """Inactive users should not be in the `users` queryset."""
        paying_user = UserFactory(membership_status=UserCustom.MembershipStatus.PAYING)
        UserFactory(membership_status=UserCustom.MembershipStatus.INACTIVE)
        self.assertQuerysetEqual(QuoteForm().fields["users"].queryset, [paying_user])

    def test_validation_error_if_both_quoted_as_and_users_missing(self):
        """
        The form should not validate if both
        `quoted_as` and `users` are missing.
        """
        data = {"quote": "Du daua", "quoted_as": "Mørke Sjeler"}

        form_valid = QuoteForm(data)
        self.assertTrue(form_valid.is_valid())

        data.pop("quoted_as")
        form_invalid = QuoteForm(data)
        self.assertFalse(form_invalid.is_valid())


class QuoteListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("quotes:QuoteList")

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class QuoteCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("quotes:QuoteCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_success_url(self):
        """Should redirect to quote list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {"quote": "Du daua", "quoted_as": "Mørke Sjeler"},
        )
        self.assertRedirects(response, reverse("quotes:QuoteList"))


class QuoteUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.quote = QuoteFactory()
        self.quote_data = {
            "quote": "Du daua",
            "quoted_as": "Mørke sjeler",
        }

    def get_url(self):
        return reverse("quotes:QuoteUpdate", args=[self.quote.pk])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to change quotes."""
        self.assertPermissionRequired(
            self.get_url(),
            "quotes.change_quote",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to change quotes.
        """
        self.client.force_login(self.quote.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_url(self):
        """Should redirect to quote list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(), self.quote_data)
        self.assertRedirects(response, reverse("quotes:QuoteList"))


class QuoteDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.quote = QuoteFactory()

    def get_url(self):
        return reverse("quotes:QuoteDelete", args=[self.quote.pk])

    def test_requires_permission(self):
        """Should require permission to delete quotes."""
        self.assertPermissionRequired(
            self.get_url(),
            "quotes.delete_quote",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete quotes.
        """
        self.client.force_login(self.quote.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_url(self):
        """Should redirect to quote list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("quotes:QuoteList"))
