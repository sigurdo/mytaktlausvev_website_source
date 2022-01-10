from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag(takes_context=True)
def get_navbar_items(context):
    """
    Returns a list of permitted navbar items, annotated with:
    - `is_active`
    - `is_dropdown`
    - `href`
    - `sub_items_annotated` - a list of subitems, annotated with:
        - `is_active`
    """
    request = context["request"]
    queryset = NavbarItem.objects.filter(parent=None).all()
    items = list(filter(lambda item: item.permitted(request.user), queryset))
    for item in items:
        item.is_active = item.active(request)
        item.is_dropdown = item.type == NavbarItem.Type.DROPDOWN
        item.href = "#" if item.is_dropdown else item.link
        item.sub_items_annotated = list(
            filter(lambda item: item.permitted(request.user), item.sub_items())
        )
        for sub_item in item.sub_items_annotated:
            sub_item.is_active = sub_item.active(request)
    return items
