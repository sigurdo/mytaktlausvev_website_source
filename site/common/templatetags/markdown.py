from django import template
from django.utils.safestring import mark_safe
import markdown as md
from markdown.inlinepatterns import SimpleTagPattern
from markdown.extensions import Extension
import bleach
from common.bootstrap_tables import BootstrapTableExtension

register = template.Library()


class StrikeThroughExtension(Extension):
    """
    Adds the possibility to use "~~something~~" to create a span that looks like <del>something</del>
    """

    RE = r"(~~)(.*?)~~"

    def extendMarkdown(self, md):
        del_tag = SimpleTagPattern(self.RE, "del")
        md.inlinePatterns.add("del", del_tag, "_begin")


class UnderlineExtension(Extension):
    """
    Adds the possibility to use "__something__" to create a span that looks like <ins>something</ins>
    """

    RE = r"(__)(.*?)__"

    def extendMarkdown(self, md):
        ins_tag = SimpleTagPattern(self.RE, "ins")
        md.inlinePatterns.add("ins", ins_tag, ">del")


ALLOWED_TAGS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "dl",
    "dt",
    "dd",
    "ul",
    "ol",
    "li",
    "table",
    "thead",
    "th",
    "tr",
    "td",
    "tbody",
    "b",
    "i",
    "u",
    "strong",
    "em",
    "small",
    "del",
    "tt",
    "span",
    "div",
    "blockquote",
    "code",
    "pre",
    "hr",
    "br",
    "a",
    "img",
    "abbr",
    "acronym",
    "br",
    "cite",
    "del",
    "ins",
]

ALLOWED_ATTRIBUTES = ["src", "alt", "width", "height", "class", "href"]


@register.filter(is_safe=True)
def markdown(string):
    converted = md.markdown(
        string,
        extensions=[
            "nl2br",
            "fenced_code",
            "codehilite",
            "tables",
            BootstrapTableExtension(),
            StrikeThroughExtension(),
            UnderlineExtension(),
        ],
    )
    bleached = bleach.clean(converted, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return mark_safe(bleached)
