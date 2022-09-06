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


ALLOWED_TAGS_INLINE_NO_LINKS = [
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
ALLOWED_ATTRIBUTES_INLINE_NO_LINKS = []


ALLOWED_TAGS_INLINE = ALLOWED_TAGS_INLINE_NO_LINKS + [
    "a",
]
ALLOWED_ATTRIBUTES_INLINE = ALLOWED_ATTRIBUTES_INLINE_NO_LINKS + ["href"]


ALLOWED_TAGS = ALLOWED_TAGS_INLINE + [
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
ALLOWED_ATTRIBUTES = ALLOWED_ATTRIBUTES_INLINE_NO_LINKS + ["src", "alt", "width", "height", "class"]


def clean_function(html, allowed_tags, allowed_attributes):
    filters = []
    if "a" in allowed_tags:
        filters.append(partial(LinkifyFilter, url_re=build_url_re(tlds=TLDS), parse_email=True))
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
        for tag, classes in filter(lambda item : item[0] in allowed_tags, full_class_map.items())
    }
    print("class map:", class_map)
    if len(class_map) > 0:
        filters.append(partial(ClassApplyFilter, class_map=class_map))
    cleaner = Cleaner(
        tags=allowed_tags,
        attributes=allowed_attributes,
        filters=filters,
    )
    bleached = cleaner.clean(html)
    return mark_safe(bleached)


@register.filter(is_safe=True)
def clean(html):
    return clean_function(html, allowed_tags=ALLOWED_TAGS, allowed_attributes=ALLOWED_ATTRIBUTES,)


@register.filter(is_safe=True)
def clean_inline(html):
    return clean_function(html, allowed_tags=ALLOWED_TAGS_INLINE, allowed_attributes=ALLOWED_ATTRIBUTES_INLINE,)


@register.filter(is_safe=True)
def clean_inline_no_links(html):
    return clean_function(html, allowed_tags=ALLOWED_TAGS_INLINE_NO_LINKS, allowed_attributes=ALLOWED_ATTRIBUTES_INLINE_NO_LINKS,)


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


def compile_markdown_inline(string):
    converted = md.markdown(
        string,
        extensions=[
            StrikethroughExtension(),
            UnderlineExtension(),
            KWordCensorExtension(),
        ],
    )
    # Strip away <p> and </p>
    converted = converted[3:-4]
    return converted


@register.filter(is_safe=True)
def markdown_inline(string):
    converted = compile_markdown_inline(string)
    return clean_inline(converted)


@register.filter(is_safe=True)
def markdown_inline_no_links(string):
    # Remove link URLs
    # Kudos to https://stackoverflow.com/questions/53980097/removing-markup-links-in-text
    string = sub(r"\[(.+?)\]\(.+?\)", r"\1", string)
    converted = compile_markdown_inline(string)
    return clean_inline_no_links(converted)
