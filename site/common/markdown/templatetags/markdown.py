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
    allowed_tags = ALLOWED_BASE_TAGS
    allowed_attributes = ALLOWED_BASE_ATTRIBUTES
    filters = []
    if allow_links:
        allowed_tags += ALLOWED_LINK_TAGS
        allowed_attributes += ALLOWED_LINK_ATTRIBUTES
        filters.append(partial(LinkifyFilter, url_re=build_url_re(tlds=TLDS), parse_email=True))
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

    Explanation of regex patterns used:

    All the patterns used are quite similar, since all matches have to start at the
    beginning of the string, with any number of directly subsequent whitespace
    characters. This part of the pattern is marked as a capture group, so that we
    can backreference it in the replacement string to preserve the whitespaces.
    Therefore, the first part of most of the regexes is (^\s*)

    To escape enumerated lists we have to insert the \ between the number and the .
    So e.g "1. Text" should be escaped with "1\. Text". Therefore, we also have to add
    \d+, meaning any number of decimal characters, but minimum 1, into the first
    capture group. 1) Can also be used to define an enumerated lists in many markdown
    implementation, but this is not the case in our library, so we don't have to
    worry about that.

    Then, after the first capture group we add the markdown operator we are escaping
    in it's own capture group. Operators that are also regex operators need another \
    to be escaped from their regex-meaning, and this \ will not be in the output
    markdown.

    Since header and list operators need to be followed by a space in order to be
    recognized as headers and lists, we add a space after the operator in the capture
    groups for these operators. Headers are apparently also recognized when followed by
    end of string, so we have to use the ( |$) subgroup.

    The `sub(pattern, replacement, string)` function replaces all occurences of the
    regex `pattern` in `string` with the regex `replacement` and returns the result.
    `replacement` can contain backreferences to capture groups in `pattern` to preserve
    them in the output.

    Our replacement string preserves both capture groups from the patterns and inserts
    a \ between them. Since \ also escapes regex, and not just markdown, we need 2 of
    them to ensure 1 is left in the markdown output.
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
    Equivalent to the markdown filter, but renders only inline markdown elements.
    The approach is simply to first escape non-inline markdown syntax, then process
    it through the regular markdown compiler, disabling extensions that are specific
    for non-inline elements, and at the end, use bleach to clean HTML-tags that are
    non-inline. This is by no means a beautiful approach, since we have to care a
    lot about so many cases of syntax we need to escape and not escape, but the
    markdown library has no support for running only the inline processor, so as per
    now, it's the best we can do.
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
