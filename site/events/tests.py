from http import HTTPStatus
from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from common.mixins import TestMixin
from accounts.factories import SuperUserFactory, UserFactory
from events.models import Event, Attendance, EventAttendance
from .factories import EventAttendanceFactory, EventFactory


class EventTestCase(TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_get_absolute_url(self):
        """Should link to the event's detail page."""
        self.assertEqual(
            self.event.get_absolute_url(),
            reverse(
                "events:detail", args=[self.event.start_time.year, self.event.slug]
            ),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.event.slug, slugify(self.event.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.event.slug
        self.event.title = "Different title"
        self.event.save()
        self.assertEqual(self.event.slug, slug_before)

    def test_creates_unique_slugs_for_events_with_same_year(self):
        """Should create unique slugs for events with the same year."""
        event_same_year = EventFactory(
            title=self.event.title,
            start_time=timezone.make_aware(datetime(self.event.start_time.year, 1, 1)),
        )
        self.assertNotEqual(self.event.slug, event_same_year.slug)

    def test_events_with_different_years_can_have_equal_slugs(self):
        """Should allow events with different years to have equal slugs."""
        event_different_year = EventFactory(
            title=self.event.title,
            start_time=timezone.make_aware(datetime(1900, 1, 1)),
        )
        self.assertEqual(self.event.slug, event_different_year.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        event = EventFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(event.slug, slug)


class EventAttendanceTestCase(TestCase):
    def setUp(self):
        self.attendance = EventAttendanceFactory()

    def test_can_only_register_attendance_once(self):
        """Should only be able to register attendance for an event once."""
        with self.assertRaises(IntegrityError):
            EventAttendanceFactory(
                event=self.attendance.event,
                person=self.attendance.person,
                status=Attendance.ATTENDING_NOT,
            )

    def test_to_str_includes_event_name(self):
        """`__str__` should include event name."""
        self.assertIn(self.attendance.event.title, str(self.attendance))

    def test_to_str_includes_user_name(self):
        """`__str__` should include the user's name."""
        self.assertIn(self.attendance.person.get_name(), str(self.attendance))

    def test_to_str_includes_status(self):
        """`__str__` should include the status."""
        self.assertIn(self.attendance.get_status_display(), str(self.attendance))


class EventDetailTestCase(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        event = EventFactory()
        self.assertLoginRequired(
            reverse("events:detail", args=[event.start_time.year, event.slug])
        )


class EventCreateTestCase(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("events:create"))

    def test_requires_permission(self):
        """Should require the `create_event` permission."""
        self.assertPermissionRequired(reverse("events:create"), "events.add_event")

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("events:create"),
            {
                "title": "A Title",
                "start_time_0": "2021-11-25",
                "start_time_1": "16:30",
                "content": "Event text",
            },
        )

        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.last()
        self.assertEqual(event.created_by, user)
        self.assertEqual(event.modified_by, user)


class EventUpdateTestCase(TestMixin, TestCase):
    def get_url(self, event):
        """Returns the URL for the event update view for `event`."""
        return reverse("events:update", args=[event.start_time.year, event.slug])

    def setUp(self):
        self.event = EventFactory()
        self.event_data = {
            "title": "A Title",
            "start_time_0": "2021-11-25",
            "start_time_1": "16:30",
            "content": "Event text",
        }

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.event))

    def test_requires_permission(self):
        """Should require the `change_event` permission."""
        self.assertPermissionRequired(
            self.get_url(self.event),
            "events.change_event",
        )

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating event."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(self.event), self.event_data)

        created_by_previous = self.event.created_by
        self.event.refresh_from_db()
        self.assertEqual(self.event.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(self.event), self.event_data)

        self.event.refresh_from_db()
        self.assertEqual(self.event.modified_by, user)


class EventAttendanceListTestCase(TestMixin, TestCase):
    def get_url(self, event):
        """Returns the URL for the event attendance list view for `event`."""
        return reverse(
            "events:attendance_list", args=[event.start_time.year, event.slug]
        )

    def setUp(self):
        self.event = EventFactory()
        EventAttendanceFactory(event=self.event)
        EventAttendanceFactory(event=self.event)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.event))

    def test_requires_permission(self):
        """Should require the `view_eventattendance` permission."""
        self.assertPermissionRequired(
            self.get_url(self.event), "events.view_eventattendance"
        )


class EventAttendanceCreateTestCase(TestMixin, TestCase):
    def get_url(self, event):
        """Returns the URL for the event attendance create view for `event`."""
        return reverse("events:attendance", args=[event.start_time.year, event.slug])

    def setUp(self):
        self.event = EventFactory()
        self.event_data = {"status": Attendance.ATTENDING_MAYBE}

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.event))

    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url(self.event))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_sets_person_to_logged_in_user(self):
        """Should set `person` to the logged in user."""
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(self.event), self.event_data)

        self.assertEqual(EventAttendance.objects.count(), 1)
        attendance = EventAttendance.objects.last()
        self.assertEqual(attendance.person, user)

    def test_sets_event_based_on_url(self):
        """Should set `event` based on URL."""
        self.client.force_login(UserFactory())
        self.client.post(self.get_url(self.event), self.event_data)

        self.assertEqual(EventAttendance.objects.count(), 1)
        attendance = EventAttendance.objects.last()
        self.assertEqual(attendance.event, self.event)

    def test_success_url_is_event(self):
        """Success URL should be the event."""
        self.client.force_login(UserFactory())
        response = self.client.post(self.get_url(self.event), self.event_data)
        self.assertRedirects(response, self.event.get_absolute_url())
