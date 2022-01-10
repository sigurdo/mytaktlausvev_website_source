from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.test import RequestFactory, TestCase

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin

from .factories import NavbarItemFactory, NavbarItemPermissionRequirementFactory
from .models import NavbarItem
from .templatetags.get_navbar_items import get_navbar_items


class NavbarItemTestSuite(TestMixin, TestCase):
    def test_to_str(self):
        link = NavbarItemFactory(text="Heim", link="/heim/")
        self.assertEqual(str(link), "Heim (/heim/)")

    def test_to_str_dropdown(self):
        dropdown = NavbarItemFactory(text="Samling", type=NavbarItem.Type.DROPDOWN)
        self.assertEqual(str(dropdown), "Samling (Nedfallsmeny)")

    def test_sub_items(self):
        """
        `sub_items()` should return all and only the sub-items of a dropdown.
        """
        item = NavbarItemFactory(type=NavbarItem.Type.DROPDOWN)
        sub_items = [NavbarItemFactory(parent=item) for _ in range(3)]
        other_items = [NavbarItemFactory() for _ in range(3)]
        for sub_item in sub_items:
            self.assertIn(sub_item, item.sub_items())
        for other_item in other_items:
            self.assertNotIn(other_item, item.sub_items())

    def test_active(self):
        """
        `active()` should return True when the provided `request_path` starts with `item.link` and False when not.
        """
        item = NavbarItemFactory(link="/hei/verden/")
        self.assertTrue(item.active("/hei/verden/"))
        self.assertTrue(item.active("/hei/verden/under/"))
        self.assertFalse(item.active("/hei/"))

    def test_permitted(self):
        """
        `permitted()` should return True when `item` is permitted for the provided user and False when not.
        """
        item = NavbarItemFactory(permissions=["navbar.add_navbaritem"])
        self.assertFalse(item.permitted(AnonymousUser()))
        self.assertFalse(item.permitted(UserFactory()))
        self.assertTrue(
            item.permitted(UserFactory(permissions=["navbar.add_navbaritem"]))
        )
        self.assertTrue(item.permitted(SuperUserFactory()))

    def test_permitted_sub_items(self):
        """
        `permitted()` should return True when `item` is permitted for the provided user and False when not.
        Same as `test_permitted`, but checks the feature that hides a dropdown when it has no permitted sub items.
        """
        dropdown = NavbarItemFactory(type=NavbarItem.Type.DROPDOWN)
        self.assertFalse(dropdown.permitted(UserFactory()))
        NavbarItemFactory(parent=dropdown, permissions=["navbar.add_navbaritem"])
        self.assertFalse(dropdown.permitted(UserFactory()))
        self.assertTrue(
            dropdown.permitted(UserFactory(permissions=["navbar.add_navbaritem"]))
        )


class NavbarItemPermissionRequirementTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.item = NavbarItemFactory(text="Heim", link="/heim/")
        self.requirement = NavbarItemPermissionRequirementFactory(
            navbar_item=self.item, permission="navbar.add_navbaritem"
        )

    def test_to_str(self):
        self.assertEqual(
            str(self.requirement),
            "Heim (/heim/) - navbar | navigasjonslinepunkt | Can add navigasjonslinepunkt",
        )

    def test_unique(self):
        """
        There should only be allowed to have one `NavbarItempermissionRequirement`
        instance for each combination of navbar_item and permission.
        """
        NavbarItemPermissionRequirementFactory(
            navbar_item=self.item, permission="navbar.change_navbaritem"
        )
        with self.assertRaises(IntegrityError):
            NavbarItemPermissionRequirementFactory(
                navbar_item=self.item, permission="navbar.change_navbaritem"
            )


class GetNavbarItemsTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.normal = NavbarItemFactory(text="Normal", link="/normal/")
        self.requires_login = NavbarItemFactory(
            text="Krev innlogging",
            link="/krev/innlogging/",
            requires_login=True,
        )
        self.requires_permission = NavbarItemFactory(
            text="Krev løyve",
            link="/krev/løyve/",
            permissions=["navbar.add_navbaritem"],
        )
        self.dropdown = NavbarItemFactory(
            text="Samling", link="/samling/", type=NavbarItem.Type.DROPDOWN
        )
        self.sub_item = NavbarItemFactory(
            text="Underpunkt", link="/underpunkt/", parent=self.dropdown
        )
        self.sub_item_restricted = NavbarItemFactory(
            text="Annet underpunkt",
            link="/annet/underpunkt/",
            parent=self.dropdown,
            requires_login=True,
        )

    def assert_annotations(
        self,
        item_annotated,
        item,
        is_active,
        is_dropdown,
        href,
        sub_items_annotated_len,
    ):
        """
        Asserts that the provided arguments are set correctly on `item_annotated`.
        """
        self.assertEqual(item_annotated, item)
        if is_active:
            self.assertTrue(item_annotated.is_active)
        else:
            self.assertFalse(item_annotated.is_active)
        if is_dropdown:
            self.assertTrue(item_annotated.is_dropdown)
        else:
            self.assertFalse(item_annotated.is_dropdown)
        self.assertEqual(item_annotated.href, href)
        self.assertEqual(
            len(item_annotated.sub_items_annotated), sub_items_annotated_len
        )

    def assert_annotations_sub(self, item_annotated, item, is_active):
        """
        Asserts that the provided arguments are set correctly on `item_annotated` for a sub-item.
        """
        self.assertEqual(item_annotated, item)
        if is_active:
            self.assertTrue(item_annotated.is_active)
        else:
            self.assertFalse(item_annotated.is_active)

    def test_unauthenticated(self):
        """
        Assert entire output from `get_navbar_items` for an AnonymousUser.
        """
        request = RequestFactory().get("/normal/noe/undergreier/")
        request.user = AnonymousUser()
        context = {"request": request}
        navbar_items = get_navbar_items(context)
        self.assertEqual(len(navbar_items), 2)
        self.assert_annotations(
            item_annotated=navbar_items[0],
            item=self.normal,
            is_active=True,
            is_dropdown=False,
            href="/normal/",
            sub_items_annotated_len=0,
        )
        self.assert_annotations(
            item_annotated=navbar_items[1],
            item=self.dropdown,
            is_active=False,
            is_dropdown=True,
            href="#",
            sub_items_annotated_len=1,
        )
        self.assert_annotations_sub(
            item_annotated=navbar_items[1].sub_items_annotated[0],
            item=self.sub_item,
            is_active=False,
        )

    def test_normal_user(self):
        """
        Assert output from `get_navbar_items` that is different from in
        `test_unauthenticated` for a regular user.
        """
        request = RequestFactory().get("/normal/noe/undergreier/")
        request.user = UserFactory()
        context = {"request": request}
        navbar_items = get_navbar_items(context)
        self.assertEqual(len(navbar_items), 3)
        self.assert_annotations(
            item_annotated=navbar_items[1],
            item=self.requires_login,
            is_active=False,
            is_dropdown=False,
            href="/krev/innlogging/",
            sub_items_annotated_len=0,
        )
        self.assert_annotations_sub(
            item_annotated=navbar_items[2].sub_items_annotated[1],
            item=self.sub_item_restricted,
            is_active=False,
        )

    def test_superuser(self):
        """
        Assert output from `get_navbar_items` that is different from in
        `test_normal_user` for a superuser.
        """
        request = RequestFactory().get("/normal/noe/undergreier/")
        request.user = SuperUserFactory()
        context = {"request": request}
        navbar_items = get_navbar_items(context)
        self.assertEqual(len(navbar_items), 4)
        self.assert_annotations(
            item_annotated=navbar_items[2],
            item=self.requires_permission,
            is_active=False,
            is_dropdown=False,
            href="/krev/løyve/",
            sub_items_annotated_len=0,
        )
