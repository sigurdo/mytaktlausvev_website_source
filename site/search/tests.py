from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from common.tests import TestMixin


class SearchTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("search:Search")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_permanent_redirect(self):
        """Should have a permanent redirect from `/search/`."""
        self.client.force_login(UserFactory())
        response = self.client.get("/search/")
        self.assertRedirects(
            response, self.get_url(), status_code=HTTPStatus.MOVED_PERMANENTLY
        )
