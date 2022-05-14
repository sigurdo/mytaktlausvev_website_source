from functools import partial

import markdown as md
from bleach import Cleaner
from bleach.html5lib_shim import Filter
from bleach.linkifier import LinkifyFilter, build_url_re
from django import template
from django.utils.safestring import mark_safe

from common.markdown_extensions import (
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


class ClassApplyFilter(Filter):
    """Filter that applies specified classes to specified tags."""

    def __init__(self, source, class_map):
        """`class_map` must be a dict of the form `{<class_name>: <classes_to_apply>}`."""
        super().__init__(source)
        self.class_map = class_map

    def __iter__(self):
        for token in Filter.__iter__(self):
            if token["type"] in ("StartTag", "EmptyTag"):
                if token["name"] in self.class_map:
                    token["data"][(None, "class")] = self.class_map[token["name"]]
            yield token


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

    cleaner = Cleaner(
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        filters=[
            partial(LinkifyFilter, url_re=build_url_re(tlds=TLDS)),
            partial(
                ClassApplyFilter,
                class_map={
                    "table": "table table-striped",
                    "img": "img-fluid",
                    "a": "text-break",
                },
            ),
        ],
    )
    bleached = cleaner.clean(converted)
    return mark_safe(bleached)
