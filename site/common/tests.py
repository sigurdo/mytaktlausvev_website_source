from os.path import basename

import magic
from django.forms import ValidationError
from django.test import TestCase
from markdown import Markdown

from articles.factories import ArticleFactory
from articles.models import Article
from comments.factories import CommentFactory
from comments.models import Comment
from common.markdown_extensions import KWordCensorExtension
from sheetmusic.factories import PdfFactory

from .mixins import TestMixin
from .templatetags.utils import contained_in, filename, verbose_name
from .test_utils import test_image, test_pdf, test_txt_file
from .validators import FileTypeValidator


class TemplateUtilsTestSuite(TestMixin, TestCase):
    def test_verbose_name(self):
        """Should return the verbose name of the instance's model."""
        article = ArticleFactory()
        self.assertEqual(verbose_name(article), Article._meta.verbose_name)
        comment = CommentFactory(content_object=article)
        self.assertEqual(verbose_name(comment), Comment._meta.verbose_name)

    def test_filename(self):
        """Should return the base filename of a file."""
        pdf = PdfFactory()
        expected = basename(pdf.file.name)
        actual = filename(pdf.file)
        self.assertEqual(expected, actual)

    def test_contained_in_true(self):
        """Should return `True` when the list is contained in the container."""
        self.assertTrue(contained_in([1], [1, 2, 3]))
        self.assertTrue(contained_in([1, 2], [1, 2, 3]))
        self.assertTrue(contained_in([3, 1], [1, 2, 3]))
        self.assertTrue(contained_in([], [1, 2, 3]))

    def test_contained_in_false(self):
        """Should return `False` when the list isn't contained in the container."""
        self.assertFalse(contained_in([4], [1, 2, 3]))
        self.assertFalse(contained_in([1, 2, 3, 4], [1, 2, 3]))
        self.assertFalse(contained_in(["1"], [1, 2, 3]))


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


class KWordCensorTestSuite(TestCase):
    def setUp(self):
        self.md = Markdown(extensions=[KWordCensorExtension()])

    def test_case_insensitive_censor(self):
        """Censor should be case-insensitive."""
        self.assertEqual(self.md.convert("korps"), "<p>k****</p>")
        self.assertEqual(self.md.convert("KORPS"), "<p>K****</p>")
        self.assertEqual(self.md.convert("Korps"), "<p>K****</p>")
        self.assertEqual(self.md.convert("kOrPs"), "<p>k****</p>")

    def test_can_escape_censor(self):
        """Should be able to escape the censor with \\"""
        self.assertEqual(self.md.convert("\korps"), "<p>korps</p>")
        self.assertEqual(self.md.convert("\KORPS"), "<p>KORPS</p>")
        self.assertEqual(self.md.convert("\Korps"), "<p>Korps</p>")
        self.assertEqual(self.md.convert("\kOrPs"), "<p>kOrPs</p>")
