from django.test import TestCase

from user_files.factories import FileFactory


class EventTestCase(TestCase):
    def setUp(self):
        self.file = FileFactory()

    def test_get_absolute_url(self):
        """Should link directly to the file."""
        pass

    def test_to_str(self):
        """Should equal the file's `name`."""
        self.assertEqual(str(self.file), self.file.name)
