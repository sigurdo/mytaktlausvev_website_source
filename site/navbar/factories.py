from factory import SubFactory
from factory.django import DjangoModelFactory

from authentication.utils import find_permission_instance

from .models import NavbarItem, NavbarItemPermissionRequirement


class NavbarItemFactory(DjangoModelFactory):
    class Meta:
        model = NavbarItem

    text = "Heim"
    order = 0
    type = NavbarItem.Type.LINK
    parent = None

    @classmethod
    def _create(self, *args, permissions=[], **kwargs):
        instance = super()._create(*args, **kwargs)
        for permission in permissions:
            NavbarItemPermissionRequirementFactory(
                navbar_item=instance,
                permission=permission,
            )
        return instance


class NavbarItemPermissionRequirementFactory(DjangoModelFactory):
    class Meta:
        model = NavbarItemPermissionRequirement

    navbar_item = SubFactory(NavbarItemFactory)

    @classmethod
    def _create(self, *args, permission="navbar.add_navbaritem", **kwargs):
        return super()._create(
            *args, permission=find_permission_instance(permission), **kwargs
        )
