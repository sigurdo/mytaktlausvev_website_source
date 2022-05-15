from django import template
from django.conf import settings

from authentication.forms import LoginForm

from ..models import NavbarItem

register = template.Library()


def get_navbar_items(user, request_path):
    """
    Returns a list of permitted navbar items, annotated with:
    - `is_active`
    - `is_dropdown`
    - `href`
    - `sub_items_annotated` - a list of subitems, annotated with:
        - `is_active`
    """
    queryset = NavbarItem.objects.filter(parent=None).all()
    items = list(filter(lambda item: item.permitted(user), queryset))
    for item in items:
        item.is_active = item.active(request_path)
        item.is_dropdown = item.type == NavbarItem.Type.DROPDOWN
        item.href = "#" if item.is_dropdown else item.link
        item.sub_items_annotated = list(
            filter(lambda item: item.permitted(user), item.sub_items())
        )
        for sub_item in item.sub_items_annotated:
            sub_item.is_active = sub_item.active(request_path)
    return items


@register.inclusion_tag("navbar/includes/navbar.html")
def navbar(user, request_path):
    return {
        "user": user,
        "request_path": request_path,
        "PRODUCTION": settings.PRODUCTION,
        "form_login": LoginForm(autofocus=False),
        "navbar_items": get_navbar_items(user, request_path),
    }
