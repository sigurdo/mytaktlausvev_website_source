from django.test import TestCase
from django.urls import reverse

from common.mixins import TestMixin
from user_files.factories import FileFactory


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
