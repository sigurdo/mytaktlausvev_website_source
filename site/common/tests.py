from os.path import basename

from django.test import TestCase

from articles.factories import ArticleFactory
from articles.models import Article
from common.comments.factories import CommentFactory
from common.comments.models import Comment
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
