from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin

from .factories import AdventCalendarFactory, WindowFactory
from .models import Window


class AdventCalendarTestSuite(TestCase):
    def setUp(self):
        self.advent_calendar = AdventCalendarFactory()

    def test_to_str(self):
        """Advent calendar `__str__` should include year."""
        self.assertEqual(
            str(self.advent_calendar), f"Julekalender {self.advent_calendar.year}"
        )

    def test_get_absolute_url(self):
        """Should link to the advent calendar's detail page."""
        self.assertEqual(
            self.advent_calendar.get_absolute_url(),
            reverse(
                "advent_calendar:AdventCalendarDetail", args=[self.advent_calendar.year]
            ),
        )


class WindowTestSuite(TestCase):
    def setUp(self):
        self.advent_calendar = AdventCalendarFactory()
        self.window = WindowFactory(advent_calendar=self.advent_calendar)

    def test_to_str(self):
        """Window `__str__` should include calendar year and window index."""
        self.assertEqual(
            str(self.window),
            f"Julekalender {self.advent_calendar.year}, luke {self.window.index}",
        )

    def test_get_absolute_url(self):
        """Should link to the window's advent calendar's detail page."""
        self.assertEqual(
            self.window.get_absolute_url(),
            reverse(
                "advent_calendar:AdventCalendarDetail",
                args=[self.window.advent_calendar.year],
            ),
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
            WindowFactory(advent_calendar=self.advent_calendar, index=self.window.index)


class AdventCalendarListTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("advent_calendar:AdventCalendarList"))


class AdventCalendarCreateTestSuite(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("advent_calendar:AdventCalendarCreate"))

    def test_requires_permission(self):
        """Should require the `add_advent_calendar` permission."""
        self.assertPermissionRequired(
            reverse("advent_calendar:AdventCalendarCreate"),
            "advent_calendar.add_adventcalendar",
        )


class AdventCalendarDetailTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.advent_calendar = AdventCalendarFactory()

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.advent_calendar.get_absolute_url())


class WindowCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.advent_calendar = AdventCalendarFactory()
        self.window_data = {"title": "Title", "content": "Christmas", "index": 15}

    def get_url(self):
        return reverse("advent_calendar:WindowCreate", args=[self.advent_calendar.year])

    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_sets_calendar_based_on_url(self):
        """Should set the window's calendar based on the URL."""
        self.client.force_login(SuperUserFactory())
        self.client.post(
            self.get_url(),
            self.window_data,
        )

        self.assertEqual(Window.objects.count(), 1)
        window = Window.objects.last()
        self.assertEqual(window.advent_calendar, self.advent_calendar)


class WindowUpdateTestSuite(TestMixin, TestCase):
    def get_url(self, window):
        """Returns the URL for the window update view for `window`."""
        return reverse(
            "advent_calendar:WindowUpdate",
            args=[window.advent_calendar.year, window.index],
        )

    def setUp(self):
        self.author = UserFactory()
        self.window = WindowFactory(created_by=self.author)
        self.window_data = {"title": "Title", "content": "Some content."}

    def test_returns_404_if_window_not_exist(self):
        """Should return 404 if the window doesn't exist."""
        response = self.client.get(
            reverse("advent_calendar:WindowUpdate", args=[1337, 15])
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.window))

    def test_requires_permission(self):
        """Should require the `change_window` permission."""
        self.assertPermissionRequired(
            self.get_url(self.window), "advent_calendar.change_window"
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_window` permission.
        """
        self.client.force_login(self.author)
        response = self.client.get(self.get_url(self.window))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirects_to_calendar(self):
        """Should redirect to the window's calendar on success."""
        self.client.force_login(self.author)
        response = self.client.post(self.get_url(self.window), self.window_data)
        self.assertRedirects(response, self.window.advent_calendar.get_absolute_url())


class WindowDeleteTestCase(TestMixin, TestCase):
    def setUp(self):
        self.window = WindowFactory()

    def get_url(self):
        return reverse(
            "advent_calendar:WindowDelete",
            args=[self.window.advent_calendar.year, self.window.index],
        )

    def test_should_redirect_to_calendar_on_success(self):
        """Should redirect to the advent calendar on success."""
        self.client.force_login(self.window.created_by)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, self.window.advent_calendar.get_absolute_url())

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to delete windows."""
        self.assertPermissionRequired(
            self.get_url(),
            "advent_calendar.delete_window",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete windows.
        """
        self.client.force_login(self.window.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)
