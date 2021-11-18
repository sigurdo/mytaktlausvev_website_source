from django.test import TestCase
from .templatetags.utils import verbose_name
from articles.models import Article
from articles.factories import ArticleFactory
from comments.models import Comment
from comments.factories import CommentFactory


class VerboseNameTest(TestCase):
    def test_verbose_name(self):
        """Should return the verbose name of the instance's model."""
        article = ArticleFactory()
        self.assertEqual(verbose_name(article), Article._meta.verbose_name)
        comment = CommentFactory(content_object=article)
        self.assertEqual(verbose_name(comment), Comment._meta.verbose_name)
