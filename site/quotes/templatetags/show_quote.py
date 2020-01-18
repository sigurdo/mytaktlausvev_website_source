"""Template-tags using quotes"""
from django import template

register = template.Library()


@register.inclusion_tag("quotes/quote.html")
def show_quote(quote):
    """Template-tag showing a single quote"""
    return {'quote': quote}
