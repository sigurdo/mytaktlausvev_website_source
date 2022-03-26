from ast import parse
from curses import tigetflag
from os.path import basename
from urllib.parse import urlencode

from django import template
from django.utils.dateparse import parse_datetime

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
