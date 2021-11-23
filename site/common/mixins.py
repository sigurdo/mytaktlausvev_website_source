from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from accounts.factories import UserFactory


class TestMixin(TestCase):
    def assertLoginRequired(self, url):
        """
        Asserts that `url` requires login by checking for a redirect to the `login` view.
        Logs out before checking.
        """
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def assertPermissionRequired(self, url, *permissions):
        """Asserts that `url` requires `permission`."""
        self.client.force_login(UserFactory())
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        self.client.force_login(UserFactory(permissions=permissions))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
