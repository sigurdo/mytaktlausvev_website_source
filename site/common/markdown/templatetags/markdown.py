import re
from functools import partial

import markdown as md
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter, build_url_re
from bs4 import BeautifulSoup, NavigableString
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


@register.filter(is_safe=True)
def truncate_html_to_number_of_words(html, number_of_words):
    """
    Returns `html` truncated to maximum `number_of_words`.

    Intelligently parses HTML and truncates based on number of words in the actual content,
    not including neither attributes, nor tag text. End tags are also preserved after the
    truncation point.

    Also adds an ellipsis and cleans the output HTML.
    """
    soup = BeautifulSoup(html, "html.parser")

    def truncate_soup(soup, word_counter):
        if type(soup) is NavigableString:
            if word_counter == number_of_words:
                return NavigableString(""), word_counter

            words = list(re.finditer(r"\w+", soup.string))
            if word_counter + len(words) <= number_of_words:
                word_counter += len(words)
                return soup, word_counter

            string_cutoff = words[number_of_words - word_counter - 1].end()
            string_to_keep = soup.string[:string_cutoff]
            if len(words) > number_of_words - word_counter:
                string_to_keep += "…"
            word_counter = number_of_words
            return NavigableString(string_to_keep), word_counter

        for child in soup.children:
            new_child, word_counter = truncate_soup(child, word_counter)
            child.replace_with(new_child)
        return soup, word_counter

    truncate_soup(soup, 0)
    # Run output through clean filter at the end to make sure it's safe
    return clean(str(soup))
