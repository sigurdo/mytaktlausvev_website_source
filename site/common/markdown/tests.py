from functools import partial

from bleach import Cleaner
from django.test import TestCase
from markdown import Markdown

from .extensions import KWordCensorExtension
from .filters import ClassApplyFilter
from .templatetags.markdown import (
    clean,
    escape_markdown_links,
    escape_non_inline_markdown,
    markdown_inline_filter,
)


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

    def test_does_not_apply_class_if_not_specified(self):
        """Should do nothing if no class has been specified for the tag."""
        cleaned = self.cleaner.clean("<span>Test!</span>")
        self.assertEqual(cleaned, "<span>Test!</span>")


class CleanTestSuite(TestCase):
    def test_allows_links_by_default(self):
        """Should allow links by default."""
        html = 'Link til <a class="text-break" href="site.com" rel="nofollow">site</a>'
        cleaned = clean(html)
        self.assertEqual(cleaned, html)

    def test_allows_blocks_by_default(self):
        """Should allow blocks by default."""
        html = "<p>Et avsnitt</p>"
        cleaned = clean(html)
        self.assertEqual(cleaned, html)

    def test_disallow_links_escapes_link(self):
        """Setting `allow_links=False` should escape links."""
        cleaned = clean("<a>site</a>", allow_links=False)
        self.assertEqual(cleaned, "&lt;a&gt;site&lt;/a&gt;")

    def test_disallow_blocks_escapes_block(self):
        """Setting `allow_blocks=False` should escape blocks."""
        cleaned = clean("<p>Avsnitt</p>", allow_blocks=False)
        self.assertEqual(cleaned, "&lt;p&gt;Avsnitt&lt;/p&gt;")

    def test_linkifies_url(self):
        cleaned = clean("Link: http://taktlaus.bet")
        self.assertEqual(
            cleaned,
            'Link: <a href="http://taktlaus.bet" rel="nofollow" class="text-break">http://taktlaus.bet</a>',
        )


class EscapeNonInlineMarkdownTestSuite(TestCase):
    def test_escapes_header(self):
        """Headers should be escaped."""
        result = escape_non_inline_markdown("# Tittel")
        self.assertEqual(result, "\\# Tittel")

    def test_escapes_header_end_of_string(self):
        """Hashtags followed by end of strings are considered headers and should be escaped."""
        result = escape_non_inline_markdown("#")
        self.assertEqual(result, "\\#")

    def test_does_not_escape_hashtag_followed_by_letters(self):
        """Hashtags followed by letters should not be escaped."""
        result = escape_non_inline_markdown("#gira")
        self.assertEqual(result, "#gira")

    def test_escapes_header_after_whitespace(self):
        """Hashtags preceded by whitespace should be escaped."""
        result = escape_non_inline_markdown("  # Tittel")
        self.assertEqual(result, "  \\# Tittel")

    def test_escapes_dash_list(self):
        """Dashed lists should be escaped."""
        result = escape_non_inline_markdown("- Tenker å mekke middag")
        self.assertEqual(result, "\\- Tenker å mekke middag")

    def test_does_not_escape_dash_followed_by_letters(self):
        """A dash followed by letters should not be escaped."""
        result = escape_non_inline_markdown("-42")
        self.assertEqual(result, "-42")

    def test_escapes_star_list(self):
        """Star lists should be escaped"""
        result = escape_non_inline_markdown("* Tenker å mekke middag")
        self.assertEqual(result, "\\* Tenker å mekke middag")

    def test_does_not_escape_star_followed_by_letters(self):
        """
        A star directly followed by letters should not be escaped.
        This is important to preserve italic text.
        """
        result = escape_non_inline_markdown("*Kremt*")
        self.assertEqual(result, "*Kremt*")

    def test_escapes_enumerated_list(self):
        """Enumerated lists should be escaped."""
        result = escape_non_inline_markdown("1. Kjøpe mat")
        self.assertEqual(result, "1\\. Kjøpe mat")

    def test_does_not_escape_decimal_and_dot_followed_by_letters(self):
        """Numbers followed by a dot and non-space characters should not be escaped."""
        result = escape_non_inline_markdown("42.3")
        self.assertEqual(result, "42.3")

    def test_escapes_block_quote(self):
        """Block quotes should be escaped."""
        result = escape_non_inline_markdown(
            "> Jeg sender mail på snapchat når jeg kommer hjem"
        )
        self.assertEqual(result, "\\> Jeg sender mail på snapchat når jeg kommer hjem")


class EscapeMarkdownLinksTestSuite(TestCase):
    def test_escapes_links(self):
        """Links should be escaped, leaving only the link text."""
        result = escape_markdown_links("En [link](til/noe) og [en link](til/noe/annet)")
        self.assertEqual(result, "En link og en link")


class MarkdownInlineFilterTestSuite(TestCase):
    def test_removes_newlines(self):
        """Eventual newlines in the input string should be replaced by spaces."""
        result = markdown_inline_filter("En\ndelt\ntekst")
        self.assertEqual(result, "En delt tekst")

    def test_removes_carriage_returns(self):
        """Eventual carriage returns in the input string should be replaced by spaces."""
        result = markdown_inline_filter("En\rdelt\rtekst")
        self.assertEqual(result, "En delt tekst")

    def test_supports_strikethrough(self):
        """Strikethrough should be supported."""
        result = markdown_inline_filter("Noe ~~gjennomstreket~~")
        self.assertEqual(result, "Noe <del>gjennomstreket</del>")

    def test_supports_underline(self):
        """Underline should be supported."""
        result = markdown_inline_filter("Noe __understreket__")
        self.assertEqual(result, "Noe <ins>understreket</ins>")

    def test_censors_k_word(self):
        """The K-word should be censored."""
        result = markdown_inline_filter("Korps er kult!")
        self.assertEqual(result, "K**** er kult!")
