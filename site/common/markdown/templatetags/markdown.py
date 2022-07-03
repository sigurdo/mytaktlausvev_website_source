from functools import partial

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
def clean(html):
    cleaner = Cleaner(
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        filters=[
            partial(LinkifyFilter, url_re=build_url_re(tlds=TLDS), parse_email=True),
            partial(
                ClassApplyFilter,
                class_map={
                    "table": "table table-striped",
                    "img": "img-fluid d-block m-auto",
                    "a": "text-break",
                    "h1": "fs-2",
                    "h2": "fs-3",
                    "h3": "fs-4",
                    "h4": "fs-5",
                    "h5": "fs-6",
                },
            ),
        ],
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
