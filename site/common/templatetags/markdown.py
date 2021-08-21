from django import template
from django.utils.safestring import mark_safe
import markdown as md
import bleach

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
]

ALLOWED_ATTRIBUTES = ["src", "alt"]


@register.filter(is_safe=True)
def markdown(string):
    converted = md.markdown(string, extensions=["nl2br"])
    bleached = bleach.clean(converted, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return mark_safe(bleached)
