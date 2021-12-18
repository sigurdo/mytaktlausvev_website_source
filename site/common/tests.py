import magic
from django.forms import ValidationError
from django.test import TestCase

from articles.factories import ArticleFactory
from articles.models import Article
from comments.factories import CommentFactory
from comments.models import Comment

from .templatetags.utils import verbose_name
from .test_utils import test_image, test_pdf, test_txt_file
from .validators import FileTypeValidator


class VerboseNameTest(TestCase):
    def test_verbose_name(self):
        """Should return the verbose name of the instance's model."""
        article = ArticleFactory()
        self.assertEqual(verbose_name(article), Article._meta.verbose_name)
        comment = CommentFactory(content_object=article)
        self.assertEqual(verbose_name(comment), Comment._meta.verbose_name)


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
