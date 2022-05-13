import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from common.mixins import TestMixin
from user_files.factories import FileFactory


class ServeAllMediaFilesTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()
        self.filename = os.path.basename(self.file.file.name)

    def get_url(self):
        return reverse(
            "serve_media_files:ServeAllMediaFiles",
            args=[f"brukarfilar/{self.filename}"],
        )

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_x_sendfile_headers(self):
        """Check that X-Sendfile headers for nginx are set correctly."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response["Content-Type"], "")
        self.assertEqual(
            response["Content-Disposition"], f'inline; filename="{self.filename}"'
        )
        self.assertEqual(
            response["X-Accel-Redirect"],
            f"{settings.MEDIA_URL_NGINX}brukarfilar/{self.filename}",
        )
