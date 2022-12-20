from django.forms import ValidationError
from django.test import TestCase

from common.test_utils import test_image, test_pdf, test_txt_file

from .validators import FileTypeValidator


class FileTypeValidatorTestSuite(TestCase):
    def setUp(self):
        self.validator = FileTypeValidator([".txt", ".pdf"])

    def test_accepted_extensions(self):
        self.validator(test_txt_file())
        self.validator(test_pdf())

    def test_wrong_extension(self):
        with self.assertRaises(ValidationError):
            self.validator(test_image())
