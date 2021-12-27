import shutil
import tempfile
from http import HTTPStatus

from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.factories import UserFactory

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestMixin(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        return super().tearDownClass()

    def assertLoginRequired(self, url):
        """
        Asserts that `url` requires login by checking for a redirect to the `login` view.
        Logs out before checking.
        """
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def assertPermissionRequired(
        self, url, *permissions, method="get", status_ok=HTTPStatus.OK
    ):
        """Asserts that `url` requires `permission`."""
        self.client.force_login(UserFactory())
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        self.client.force_login(UserFactory(permissions=permissions))
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, status_ok)
