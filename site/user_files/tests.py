from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from common.test_utils import test_txt_file

from .factories import FileFactory
from .models import File


class FileTestCase(TestMixin, TestCase):
    def setUp(self):
        self.file = FileFactory()

    def test_get_absolute_url(self):
        """Should link directly to the file."""
        self.assertEqual(self.file.get_absolute_url(), self.file.file.url)

    def test_to_str(self):
        """Should equal the file's `name`."""
        self.assertEqual(str(self.file), self.file.name)


class FileListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("user_files:FileList")

    def test_login_required(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class FileCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("user_files:FileCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertEqual(File.objects.count(), 1)
        files = File.objects.last()
        self.assertEqual(files.created_by, user)
        self.assertEqual(files.modified_by, user)

    def test_redirects_to_file_list_on_success(self):
        """Should redirect to the file list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(),
            {"name": "616.mp3", "file": test_txt_file()},
        )

        self.assertRedirects(response, reverse("user_files:FileList"))
