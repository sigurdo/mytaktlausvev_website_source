from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from minutes.factories import MinutesFactory
from minutes.models import Minutes


class EventTestCase(TestCase):
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


class MinutesListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("minutes:MinutesList")

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class MinutesDetailTestCase(TestMixin, TestCase):
    def setUp(self):
        self.minutes = MinutesFactory()

    def get_url(self):
        return reverse("minutes:MinutesDetail", args=[self.minutes.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class MinutesCreateTestCase(TestMixin, TestCase):
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
