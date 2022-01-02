from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag()
def navbar_item_is_active(navbar_item, request):
    """Returns True if navbar_item is active and False if not."""
    request_path = request.path.split("/")
    match navbar_item.type:
        case NavbarItem.Type.LINK:
            item_paths = [navbar_item.link.split("/")]
        case NavbarItem.Type.DROPDOWN:
            item_paths = [subitem.link.split("/") for subitem in navbar_item.children.all()]
        case _:
            item_paths = []

    def compare_paths(item_path, request_path):
        if len(request_path) < len(item_path):
            return False
        for i in range(len(item_path)):
            if request_path[i] != item_path[i]:
                return False
        return True

    for item_path in item_paths:
        if compare_paths(item_path, request_path):
            return True
    return False
