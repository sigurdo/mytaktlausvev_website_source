from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag()
def get_navbar_items():
    """Returns a list of all navbar items."""
    return NavbarItem.objects.all()
