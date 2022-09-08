from functools import partial
from re import sub

import markdown as md
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter, build_url_re
from django import template
from django.utils.safestring import mark_safe

from ..extensions import (
    KWordCensorExtension,
    StrikethroughExtension,
    UnderlineExtension,
)
from ..filters import ClassApplyFilter
from ..tlds import TLDS

register = template.Library()


ALLOWED_BASE_TAGS = [
    "b",
    "strong",
    "i",
    "cite",
    "em",
    "u",
    "ins",
    "del",
    "small",
    "span",
]
ALLOWED_BASE_ATTRIBUTES = []

ALLOWED_LINK_TAGS = ["a"]
ALLOWED_LINK_ATTRIBUTES = ["href"]

ALLOWED_BLOCK_TAGS = [
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
    "tbody",
    "th",
    "tr",
    "td",
    "tt",
    "div",
    "blockquote",
    "code",
    "pre",
    "hr",
    "br",
    "img",
    "abbr",
    "acronym",
]
ALLOWED_BLOCK_ATTRIBUTES = ["src", "alt", "width", "height", "class"]


def get_class_apply_filter(allowed_tags):
    full_class_map = {
        "table": "table table-striped",
        "img": "img-fluid d-block m-auto",
        "a": "text-break",
        "h1": "fs-2",
        "h2": "fs-3",
        "h3": "fs-4",
        "h4": "fs-5",
        "h5": "fs-6",
    }
    class_map = {
        tag: classes
        for tag, classes in filter(
            lambda item: item[0] in allowed_tags, full_class_map.items()
        )
    }
    return partial(ClassApplyFilter, class_map=class_map)


def clean(html, allow_links=True, allow_blocks=True):
    allowed_tags = ALLOWED_BASE_TAGS.copy()
    allowed_attributes = ALLOWED_BASE_ATTRIBUTES.copy()
    filters = []
    if allow_links:
        allowed_tags += ALLOWED_LINK_TAGS
        allowed_attributes += ALLOWED_LINK_ATTRIBUTES
        filters.append(
            partial(LinkifyFilter, url_re=build_url_re(tlds=TLDS), parse_email=True)
        )
    if allow_blocks:
        allowed_tags += ALLOWED_BLOCK_TAGS
        allowed_attributes += ALLOWED_BLOCK_ATTRIBUTES
    filters.append(get_class_apply_filter(allowed_tags))
    cleaner = Cleaner(
        tags=allowed_tags,
        attributes=allowed_attributes,
        filters=filters,
    )
    bleached = cleaner.clean(html)
    return mark_safe(bleached)


@register.filter(is_safe=True)
def markdown(string):
    converted = md.markdown(
        string,
        extensions=[
            "nl2br",
            "fenced_code",
            "codehilite",
            "tables",
            StrikethroughExtension(),
            UnderlineExtension(),
            KWordCensorExtension(),
        ],
    )
    return clean(converted)


def escape_non_inline_markdown(string):
    """
    Escape non-inline markdown operators that are likely to occur unintentionally
    in inline text. Escaping is done by adding a \ before the operator, so that
    e.g. "# Unintentional header" becomes "\# Unintentional header". Input string
    is assumed to not contain any newlines.

    Logic behind regex patterns is described on the wiki,
    https://gitlab.com/taktlause/taktlausveven/-/wikis/Markdown
    """

    patterns = [
        # Headers
        r"(^\s*)(#( |$))",
        # Lists
        r"(^\s*)(- )",
        r"(^\s*)(\* )",
        # Enumerated lists
        r"(^\s*\d+)(\. )",
        # Block quotes
        r"(^\s*)(>)",
    ]

    for pattern in patterns:
        string = sub(pattern, r"\1\\\2", string)

    return string


def escape_markdown_links(string):
    """
    Escapes markdown links, leaving only the link text.
    Kudos to https://stackoverflow.com/questions/53980097/removing-markup-links-in-text
    """
    return sub(r"\[(.+?)\]\(.+?\)", r"\1", string)


def markdown_inline_filter(string, allow_links=True):
    """
    Equivalent to the `markdown` filter, but renders only inline markdown elements.

    A more detailed description can be found on the wiki,
    https://gitlab.com/taktlause/taktlausveven/-/wikis/Markdown
    """

    # Replace eventual newlines and carriage returns with spaces.
    string = " ".join(string.split("\n"))
    string = " ".join(string.split("\r"))

    string = escape_non_inline_markdown(string)

    if not allow_links:
        string = escape_markdown_links(string)

    converted = md.markdown(
        string,
        extensions=[
            StrikethroughExtension(),
            UnderlineExtension(),
            KWordCensorExtension(),
        ],
    )

    # Strip away <p> and </p>
    converted = sub(r"^<p>(.*)</p>$", r"\1", converted)

    if allow_links:
        bleached = clean(converted, allow_blocks=False)
    else:
        bleached = clean(converted, allow_links=False, allow_blocks=False)

    return bleached


@register.filter(is_safe=True)
def markdown_inline(string):
    return markdown_inline_filter(string)


@register.filter(is_safe=True)
def markdown_inline_no_links(string):
    return markdown_inline_filter(string, allow_links=False)
