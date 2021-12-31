from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag()
def navbar_item_is_active(navbar_item, request):
    """Returns True if navbar_item is active and False if not."""
    request_path = request.path.split("/")
    item_path = navbar_item.link.split("/")
    if len(request_path) < len(item_path):
        return False
    for i in range(len(item_path)):
        if request_path[i] != item_path[i]:
            return False
    return True
