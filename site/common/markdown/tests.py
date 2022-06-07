from functools import partial

from bleach import Cleaner
from django.test import TestCase
from markdown import Markdown

from .extensions import KWordCensorExtension
from .filters import ClassApplyFilter
from .templatetags.markdown import clean, truncate_html_to_number_of_words


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


class TruncateHtmlToNumberOfWordsTestSuite(TestCase):
    def test_truncate_html_to_number_of_words(self):
        """
        Should truncate `html` with truncation point between the words "cut" and
        "off" inside the link.
        """
        html = """
<p> Paragraph. </p>
Text in between.
<ul>
    <li>
        <a href="/a/link/"> A link that is cut off. </a>
    </li>
</ul>
Some more text here that is removed.
"""
        truncated = truncate_html_to_number_of_words(html, 9)
        self.assertEqual(
            truncated,
            clean(
                """
<p> Paragraph. </p>
Text in between.
<ul>
<li>
<a href="/a/link/"> A link that is cut…</a></li></ul>"""
            ),
        )
