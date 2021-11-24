from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from accounts.factories import SuperUserFactory
from common.mixins import TestMixin
from .factories import JulekalenderFactory, WindowFactory
from .models import Window


class JulekalenderTestSuite(TestCase):
    def setUp(self):
        self.julekalender = JulekalenderFactory()

    def test_to_str(self):
        """Julekalender `__str__` should include year."""
        self.assertEqual(
            str(self.julekalender), f"Julekalender {self.julekalender.year}"
        )

    def test_get_absolute_url(self):
        """Should link to the julekalender's detail page."""
        self.assertEqual(
            self.julekalender.get_absolute_url(),
            reverse("julekalender:detail", args=[self.julekalender.year]),
        )


class WindowTestSuite(TestCase):
    def setUp(self):
        self.julekalender = JulekalenderFactory()
        self.window = WindowFactory(calendar=self.julekalender)

    def test_to_str(self):
        """Window `__str__` should include calendar year and window index."""
        self.assertEqual(
            str(self.window),
            f"Julekalender {self.julekalender.year}, luke {self.window.index}",
        )

    def test_get_absolute_url(self):
        """Should link to the window's julekalender's detail page."""
        self.assertEqual(
            self.window.get_absolute_url(),
            reverse("julekalender:detail", args=[self.window.calendar.year]),
        )

    def test_index_cannot_be_lower_than_1(self):
        """Should not allow window index lower than 1."""
        with self.assertRaises(ValidationError):
            WindowFactory(index=0).full_clean()
        with self.assertRaises(ValidationError):
            WindowFactory(index=-50).full_clean()

    def test_index_cannot_be_higher_than_24(self):
        """Should not allow window index higher than 24."""
        with self.assertRaises(ValidationError):
            WindowFactory(index=25).full_clean()
        with self.assertRaises(ValidationError):
            WindowFactory(index=350).full_clean()

    def test_calendar_and_index_unique_together(self):
        """Calendar and index must be unique together."""
        with self.assertRaises(IntegrityError):
            WindowFactory(calendar=self.julekalender, index=self.window.index)


class JulekalenderListTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("julekalender:list"))


class JulekalenderCreateTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("julekalender:create"))

    def test_requires_permission(self):
        """Should require the `add_julekalender` permission."""
        self.assertPermissionRequired(
            reverse("julekalender:create"), "julekalender.add_julekalender"
        )


class JulekalenderDetailTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.julekalender = JulekalenderFactory()

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.julekalender.get_absolute_url())


class WindowCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.julekalender = JulekalenderFactory()
        self.window_data = {"title": "Title", "content": "Christmas", "index": 15}

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(
            reverse("julekalender:window_create", args=[self.julekalender.year])
        )

    def test_sets_calendar_based_on_url(self):
        """Should set the window's calendar based on the URL."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("julekalender:window_create", args=[self.julekalender.year]),
            self.window_data,
        )

        self.assertEqual(Window.objects.count(), 1)
        window = Window.objects.last()
        self.assertEqual(window.calendar, self.julekalender)

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("julekalender:window_create", args=[self.julekalender.year]),
            self.window_data,
        )

        self.assertEqual(Window.objects.count(), 1)
        window = Window.objects.last()
        self.assertEqual(window.created_by, user)
        self.assertEqual(window.modified_by, user)
