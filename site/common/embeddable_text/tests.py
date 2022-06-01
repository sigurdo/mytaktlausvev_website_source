from django.db import IntegrityError
from django.test import TestCase

from common.mixins import TestMixin

from .factories import EmbeddableTextFactory
from .models import EmbeddableText


class EmbeddableTextTestSuite(TestMixin, TestCase):
    def test_to_str(self):
        text = EmbeddableTextFactory(name="example_text")
        self.assertEqual(str(text), "example_text")

    def test_content_blank_by_default(self):
        """Default `content` should be an empty string."""
        text = EmbeddableTextFactory()
        self.assertEqual(text.content, "")

    def test_name_unique(self):
        """`name` must be unique."""
        text = EmbeddableTextFactory()
        with self.assertRaises(IntegrityError):
            EmbeddableTextFactory(name=text.name)

    def test_ordering(self):
        """`EmbeddableText`s should be ordered by name."""
        self.assertModelOrdering(
            EmbeddableText,
            EmbeddableTextFactory,
            [
                {"name": "text_a"},
                {"name": "text_b"},
            ],
        )
