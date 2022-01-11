from factory import SubFactory, post_generation, sequence
from factory.django import DjangoModelFactory

from authentication.utils import find_permission_instance

from .models import NavbarItem, NavbarItemPermissionRequirement


class NavbarItemFactory(DjangoModelFactory):
    class Meta:
        model = NavbarItem

    text = "Heim"
    order = sequence(lambda n: n)
    type = NavbarItem.Type.LINK
    parent = None

    @post_generation
    def permissions(self, create, permissions):
        if not create or not permissions:
            return

        for permission in permissions:
            NavbarItemPermissionRequirementFactory(
                navbar_item=self,
                permission=permission,
            )


class NavbarItemPermissionRequirementFactory(DjangoModelFactory):
    class Meta:
        model = NavbarItemPermissionRequirement

    navbar_item = SubFactory(NavbarItemFactory)

    @classmethod
    def _create(self, *args, permission="navbar.add_navbaritem", **kwargs):
        return super()._create(
            *args, permission=find_permission_instance(permission), **kwargs
        )
