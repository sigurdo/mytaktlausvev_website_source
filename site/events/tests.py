from django.test import TestCase
from django.db import IntegrityError
from django.urls import reverse
from django.utils.text import slugify
from common.mixins import TestMixin
from events.models import Attendance
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
