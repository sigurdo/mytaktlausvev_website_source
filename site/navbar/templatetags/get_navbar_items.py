from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag(takes_context=True)
def get_navbar_items(context):
    """Returns a list of all navbar items, annotated with `is_active` and `is_permitted`."""
    request = context["request"]
    items = NavbarItem.objects.filter(parent=None).all()
    for item in items:
        item.is_active = item.active(request)
        item.is_permitted = item.permitted(request.user)
        item.sub_items_annotated = item.sub_items()
        for sub_item in item.sub_items_annotated:
            sub_item.is_active = sub_item.active(request)
            sub_item.is_permitted = sub_item.permitted(request.user)
    return items
