from datetime import date, datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware, now

from accounts.factories import UserFactory
from articles.factories import ArticleFactory
from common.comments.factories import CommentFactory
from common.constants.models import Constant
from common.mixins import TestMixin
from events.factories import EventFactory
from events.models import Event
from minutes.factories import MinutesFactory
from pictures.factories import GalleryFactory, ImageFactory


class DashboardRedirectTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("dashboard:DashboardRedirect")

    def test_not_logged_in(self):
        """Should redirect to the configured guest start page when not logged in."""
        Constant.objects.create(name="Gjestestartside", value="https://example.com")
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, "https://example.com", fetch_redirect_response=False
        )

    def test_logged_in(self):
        """Should redirect to the dashboard when logged in."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertRedirects(response, reverse("dashboard:Dashboard"))


class DashboardTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("dashboard:Dashboard")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def get_context(self):
        self.client.force_login(UserFactory())
        return self.client.get(self.get_url()).context

    def test_latest_quotes_in_context(self):
        context = self.get_context()
        self.assertIn("latest_quotes", context)

    def test_random_quotes_in_context(self):
        context = self.get_context()
        self.assertIn("random_quotes", context)

    def test_events_in_context(self):
        EventFactory()
        context = self.get_context()
        self.assertIn("events", context)
        self.assertEquals(len(list(context["events"])), 1)

    def test_shows_all_events_upcoming_the_next_month(self):
        """Should should all events happening the next month."""
        for _ in range(10):
            EventFactory(start_time=now())
            EventFactory(start_time=now() + timedelta(days=365))

        context = self.get_context()
        self.assertIn("events", context)
        self.assertQuerysetEqual(
            context["events"],
            Event.objects.upcoming().filter(start_time__lte=now() + timedelta(days=31)),
        )

    def test_shows_5_events_if_less_than_five_the_next_month(self):
        """
        Should show up to 5 events happening later than the next month,
        if there are less than 5 upcoming events the next month.
        """
        for _ in range(10):
            EventFactory(start_time=now() + timedelta(days=365))

        context = self.get_context()
        self.assertIn("events", context)
        self.assertQuerysetEqual(context["events"], Event.objects.upcoming()[:5])

    def test_shows_all_upcoming_events_if_5_or_less_upcoming(self):
        """Should show all upcoming events if there are less than 5 upcoming events."""
        for _ in range(3):
            EventFactory(start_time=now())

        context = self.get_context()
        self.assertIn("events", context)
        self.assertQuerysetEqual(context["events"], Event.objects.upcoming())

    def test_minutes_ordered_by_created_date(self):
        minutes = [
            MinutesFactory(),
            MinutesFactory(date=date.today() + timedelta(days=1)),
            MinutesFactory(date=date.today() - timedelta(days=1)),
        ]
        minutes.reverse()
        self.assertQuerysetEqual(minutes, self.get_context()["minutes"])

    def test_latest_galleries_in_context(self):
        ImageFactory()
        context = self.get_context()
        self.assertIn("latest_galleries", context)
        self.assertEquals(len(list(context["latest_galleries"])), 1)

    def test_latest_galleries_excludes_empty(self):
        GalleryFactory()
        context = self.get_context()
        self.assertEquals(len(list(context["latest_galleries"])), 0)

    def test_random_images_in_context(self):
        context = self.get_context()
        self.assertIn("random_images", context)

    def test_random_images_does_not_include_new_image(self):
        ImageFactory()
        context = self.get_context()
        self.assertEquals(len(list(context["random_images"])), 0)

    def test_random_images_includes_3_year_old_image(self):
        image = ImageFactory()
        image.uploaded = make_aware(datetime.now() - timedelta(days=3 * 365))
        image.save()
        context = self.get_context()
        self.assertEquals(len(list(context["random_images"])), 1)

    def test_random_images_does_not_includes_10_year_old_image(self):
        ImageFactory(uploaded=make_aware(datetime.now() - timedelta(days=10 * 365)))
        context = self.get_context()
        self.assertEquals(len(list(context["random_images"])), 0)

    def test_latest_comments_in_context(self):
        CommentFactory(content_object=ArticleFactory())
        context = self.get_context()
        self.assertIn("latest_comments", context)
        self.assertEquals(len(list(context["latest_comments"])), 1)
