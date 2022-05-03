from functools import partial

import markdown as md
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter, build_url_re
from django import template
from django.utils.safestring import mark_safe

from common.markdown_extensions import (
    BootstrapTableExtension,
    KWordCensorExtension,
    StrikethroughExtension,
    UnderlineExtension,
)
from common.tlds import TLDS

register = template.Library()


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


def set_text_break(attrs, new=False):
    attrs[(None, "class")] = "text-break"
    return attrs


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
            StrikethroughExtension(),
            UnderlineExtension(),
            KWordCensorExtension(),
        ],
    )

    cleaner = Cleaner(
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        filters=[
            partial(
                LinkifyFilter,
                url_re=build_url_re(tlds=TLDS),
                callbacks=[set_text_break],
            )
        ],
    )
    bleached = cleaner.clean(converted)
    return mark_safe(bleached)
