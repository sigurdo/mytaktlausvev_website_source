from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag()
def navbar_item_is_permitted(navbar_item, user):
    """Returns `True` if `user` is permitted to access `navbar_item` and `False` if not."""
    if navbar_item.requires_login and not user.is_authenticated:
        return False
    for permission_requirement in navbar_item.permission_requirements.all():
        permission = permission_requirement.permission
        permission_string = f"{permission.content_type.app_label}.{permission.codename}"
        if not user.has_perm(permission_string):
            return False
    return navbar_item.type == NavbarItem.Type.LINK or all(
        navbar_item_is_permitted(subitem, user)
        for subitem in navbar_item.children.all()
    )
