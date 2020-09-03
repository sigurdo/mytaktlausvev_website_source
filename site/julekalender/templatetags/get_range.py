from django import template

register = template.Library()


@register.filter
def get_range(stop):
    return range(stop)
