from factory.django import DjangoModelFactory

from .models import NavbarItem


class NavbarItemFactory(DjangoModelFactory):
    class Meta:
        model = NavbarItem

    text = "Heim"
    order = 0
    type = NavbarItem.Type.LINK
    parent = None
