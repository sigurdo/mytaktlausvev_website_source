from os.path import basename

from django import template
from django.templatetags.static import static
from django.utils.dateparse import parse_datetime
from django.utils.safestring import mark_safe

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


@register.filter
def embed_pdf_url(pdf_url):
    return mark_safe(f"{static('js/pdf.js/web/viewer.html')}?file={pdf_url}")
