from datetime import date
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from minutes.factories import MinutesFactory
from minutes.models import Minutes


class MinutesTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.minutes = MinutesFactory()

    def test_get_absolute_url(self):
        """Should link to the minutes' detail page."""
        self.assertEqual(
            self.minutes.get_absolute_url(),
            reverse("minutes:MinutesDetail", args=[self.minutes.slug]),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.minutes.slug, slugify(self.minutes.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.minutes.slug
        self.minutes.title = "Different title"
        self.minutes.save()
        self.assertEqual(self.minutes.slug, slug_before)

    def test_creates_unique_slugs(self):
        """Should create unique slugs even if titles match."""
        minutes_same_title = MinutesFactory(title=self.minutes.title)
        self.assertNotEqual(self.minutes.slug, minutes_same_title.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        minutes = MinutesFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(minutes.slug, slug)

    def test_date_defaults_to_today(self):
        """`date` should default to the current date."""
        self.assertEqual(self.minutes.date, date.today())

    def test_ordering(self):
        """Should be ordered by `date`, descending."""
        self.assertModelOrdering(
            Minutes,
            MinutesFactory,
            [
                {"date": date(2022, 5, 3), "title": "Newest"},
                {"date": date(2022, 5, 2), "title": "Middle"},
                {"date": date(2019, 6, 22), "title": "Oldest"},
            ],
        )


class MinutesListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("minutes:MinutesList")

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class MinutesDetailTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.minutes = MinutesFactory()

    def get_url(self):
        return reverse("minutes:MinutesDetail", args=[self.minutes.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class MinutesCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("minutes:MinutesCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {
                "title": "Another Meeting",
                "content": "Bureaucracy...",
                "date": date.today(),
            },
        )

        self.assertEqual(Minutes.objects.count(), 1)
        minutes = Minutes.objects.last()
        self.assertEqual(minutes.created_by, user)
        self.assertEqual(minutes.modified_by, user)


class MinutesUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.minutes = MinutesFactory()
        self.minutes_data = {
            "title": "Another one",
            "content": "Again! Again! Again!",
            "date": date.today(),
        }

    def get_url(self):
        return reverse("minutes:MinutesUpdate", args=[self.minutes.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to change minutes."""
        self.assertPermissionRequired(
            self.get_url(),
            "minutes.change_minutes",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to change minutes.
        """
        self.client.force_login(self.minutes.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating minutes."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.minutes_data)

        created_by_previous = self.minutes.created_by
        self.minutes.refresh_from_db()
        self.assertEqual(self.minutes.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.minutes_data)

        self.minutes.refresh_from_db()
        self.assertEqual(self.minutes.modified_by, user)


class MinutesDeleteTestCase(TestMixin, TestCase):
    def setUp(self):
        self.minutes = MinutesFactory()

    def get_url(self):
        return reverse("minutes:MinutesDelete", args=[self.minutes.slug])

    def test_should_redirect_to_minutes_list_on_success(self):
        """Should redirect to the minutes list on success."""
        self.client.force_login(self.minutes.created_by)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("minutes:MinutesList"))

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to delete minutes."""
        self.assertPermissionRequired(
            self.get_url(),
            "minutes.delete_minutes",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete minutes.
        """
        self.client.force_login(self.minutes.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)
