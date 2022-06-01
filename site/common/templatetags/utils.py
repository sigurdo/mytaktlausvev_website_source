import re
from os.path import basename

from bs4 import BeautifulSoup, NavigableString
from django import template
from django.utils.dateparse import parse_datetime

from common.markdown.templatetags.markdown import clean

register = template.Library()


@register.filter()
def verbose_name(model_instance):
    """Returns the verbose name of `model_instance`'s model."""
    return model_instance._meta.verbose_name


@register.filter
def get_range(length):
    """Returns a range from 0 to `length`, exclusive."""
    return range(length)


@register.filter
def filename(file):
    return basename(file.name)


@register.filter
def contained_in(list, container):
    """Returns whether all elements of `list` are also in `container`."""
    return all(element in container for element in list)


@register.filter
def parse_iso8601(value):
    return parse_datetime(value)


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
            string_to_keep = soup.string[
                : words[number_of_words - word_counter - 1].end()
            ]
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
