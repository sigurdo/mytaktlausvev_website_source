from django import template

from ..models import NavbarItem

register = template.Library()


@register.simple_tag()
def navbar_item_is_permitted(navbar_item, user):
    """Returns `True` if `user` is permitted to access `navbar_item` and `False` if not."""
    for permission_requirement in navbar_item.permission_requirements.all():
        permission = permission_requirement.permission
        permission_string = f"{permission.content_type.app_label}.{permission.codename}"
        if not user.has_perm(permission_string):
            return False
    if navbar_item.type == NavbarItem.Type.DROPDOWN and navbar_item.children.count() > 0:
        for subitem in navbar_item.children.all():
            if navbar_item_is_permitted(subitem, user):
                return True
        return False
    return True
