from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from common.mixins import TestMixin
from accounts.factories import SuperUserFactory
from events.models import Event, Attendance
from .factories import EventAttendanceFactory, EventFactory


class EventTestCase(TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.event.slug, slugify(self.event.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.event.slug
        self.event.title = "Different title"
        self.event.save()
        self.assertEqual(self.event.slug, slug_before)

    def test_creates_unique_slugs(self):
        """Should create unique slugs even if titles match."""
        event_same_title = EventFactory(title=self.event.title)
        self.assertNotEqual(self.event.slug, event_same_title.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        event = EventFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(event.slug, slug)


class EventAttendanceTestCase(TestCase):
    def test_can_only_register_attendance_once(self):
        """Should only be able to register attendance for an event once."""
        attendance = EventAttendanceFactory()
        with self.assertRaises(IntegrityError):
            EventAttendanceFactory(
                event=attendance.event,
                person=attendance.person,
                status=Attendance.ATTENDING_NOT,
            )


class EventDetailTestCase(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        event = EventFactory()
        self.assertLoginRequired(reverse("events:detail", args=[event.slug]))


class EventCreateTestCase(TestMixin, TestCase):
    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("events:create"),
            {"title": "A Title", "start_time": timezone.now(), "content": "Event text"},
        )

        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.last()
        self.assertEqual(event.created_by, user)
        self.assertEqual(event.modified_by, user)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("events:create"))

    def test_requires_permission(self):
        """Should require the `create_event` permission."""
        self.assertPermissionRequired(reverse("events:create"), "events.add_event")


class EventUpdateTestCase(TestMixin, TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("events:update", args=[self.event.slug]))

    def test_requires_permission(self):
        """Should require the `change_event` permission."""
        self.assertPermissionRequired(
            reverse("events:update", args=[self.event.slug]),
            "events.change_event",
        )

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating event."""
        self.client.force_login(SuperUserFactory())
        self.client.post(
            reverse("events:update", args=[self.event.slug]),
            {"title": "A Title", "start_time": timezone.now(), "content": "Event text"},
        )

        created_by_previous = self.event.created_by
        self.event.refresh_from_db()
        self.assertEqual(self.event.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("events:update", args=[self.event.slug]),
            {"title": "A Title", "start_time": timezone.now(), "content": "Event text"},
        )

        self.event.refresh_from_db()
        self.assertEqual(self.event.modified_by, user)
