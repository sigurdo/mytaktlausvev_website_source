from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from accounts.factories import UserFactory
from articles.factories import ArticleFactory
from comments.factories import CommentFactory
from common.mixins import TestMixin
from events.factories import EventFactory
from minutes.factories import MinutesFactory
from pictures.factories import GalleryFactory, ImageFactory


class DashboardRedirectTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("dashboard:DashboardRedirect")

    def test_not_logged_in(self):
        ArticleFactory(slug="om-oss", public=True)
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, reverse("articles:ArticleDetail", args=["om-oss"])
        )

    def test_logged_in(self):
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

    def test_minutes_in_context(self):
        MinutesFactory()
        context = self.get_context()
        self.assertIn("minutes", context)
        self.assertEquals(len(list(context["minutes"])), 1)

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
