from functools import partial
from os.path import basename

from bleach import Cleaner
from django.test import TestCase
from markdown import Markdown

from articles.factories import ArticleFactory
from articles.models import Article
from common.comments.factories import CommentFactory
from common.comments.models import Comment
from common.markdown_extensions import KWordCensorExtension
from common.templatetags.markdown import ClassApplyFilter
from sheetmusic.factories import PdfFactory

from .mixins import TestMixin
from .templatetags.utils import contained_in, filename, verbose_name


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


class ClassApplyTestSuite(TestCase):
    def setUp(self):
        self.cleaner = Cleaner(
            tags=["p", "span"],
            attributes=["class"],
            filters=[
                partial(
                    ClassApplyFilter,
                    class_map={"p": "test"},
                ),
            ],
        )

    def test_applies_class_if_specified(self):
        """Should apply the specified classes for the tag."""
        cleaned = self.cleaner.clean("<p>Test!</p>")
        self.assertEqual(cleaned, '<p class="test">Test!</p>')

    def test_does_not_appli_class_if_not_specified(self):
        """Should do nothing if no class has been specified for the tag."""
        cleaned = self.cleaner.clean("<span>Test!</span>")
        self.assertEqual(cleaned, "<span>Test!</span>")
