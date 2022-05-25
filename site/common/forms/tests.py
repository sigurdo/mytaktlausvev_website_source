import magic
from django.forms import ValidationError
from django.test import TestCase

from common.test_utils import test_image, test_pdf, test_txt_file

from .validators import FileTypeValidator


class FileTypeValidatorTestSuite(TestCase):
    def setUp(self):
        self.validator = FileTypeValidator(
            {
                "text/plain": [".txt"],
                "application/pdf": [".pdf", ".pdfdoc"],
            }
        )

    def test_plaintext_file_type(self):
        self.assertEqual(
            magic.from_buffer(test_txt_file().read(), mime=True), "text/plain"
        )

    def test_pdf_file_type(self):
        self.assertEqual(
            magic.from_buffer(test_pdf().read(), mime=True), "application/pdf"
        )

    def test_gif_file_type(self):
        self.assertEqual(magic.from_buffer(test_image().read(), mime=True), "image/gif")

    def test_good_file(self):
        self.validator(test_txt_file())

    def test_wrong_extension(self):
        with self.assertRaises(ValidationError):
            self.validator(test_txt_file(name="test.text"))

    def test_wrong_type(self):
        with self.assertRaises(ValidationError):
            self.validator(test_image(name="test.txt"))

    def test_no_match(self):
        with self.assertRaises(ValidationError):
            self.validator(test_pdf(name="test.txt"))

    def test_multiple_extensions(self):
        self.validator(test_pdf())
        self.validator(test_pdf(name="test.pdfdoc"))

    def test_wrong_multiple_extensions(self):
        with self.assertRaises(ValidationError):
            self.validator(test_pdf(name="test.pdff"))
