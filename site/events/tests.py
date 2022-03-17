from datetime import datetime, timedelta
from http import HTTPStatus

from django.db import IntegrityError
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import make_aware, now

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from events.models import Attendance, Event, EventAttendance
from events.views import (
    event_breadcrumbs,
    get_event_attendance_or_404,
    get_event_or_404,
)

from .factories import EventAttendanceFactory, EventFactory


class EventManagerTestCase(TestCase):
    def test_upcoming_no_end_time_old(self):
        EventFactory(start_time=make_aware(datetime.now() - timedelta(2)))
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 0)

    def test_upcoming_no_end_time_last_12_hours(self):
        EventFactory(start_time=make_aware(datetime.now() - timedelta(hours=6)))
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 1)

    def test_upcoming_no_end_time_upcoming(self):
        EventFactory(start_time=make_aware(datetime.now() + timedelta(1)))
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 1)

    def test_upcoming_end_time_old(self):
        EventFactory(
            start_time=make_aware(datetime.now() - timedelta(3)),
            end_time=make_aware(datetime.now() - timedelta(2)),
        )
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 0)

    def test_upcoming_end_time_last_12_hours(self):
        EventFactory(
            start_time=make_aware(datetime.now() - timedelta(3)),
            end_time=make_aware(datetime.now() - timedelta(hours=6)),
        )
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 0)

    def test_upcoming_end_time_upcoming(self):
        EventFactory(
            start_time=make_aware(datetime.now() - timedelta(3)),
            end_time=make_aware(datetime.now() + timedelta(1)),
        )
        upcoming = list(Event.objects.upcoming())
        self.assertEqual(len(upcoming), 1)


class EventTestCase(TestCase):
    def setUp(self):
        self.event = EventFactory()

    def test_get_absolute_url(self):
        """Should link to the event's detail page."""
        self.assertEqual(
            self.event.get_absolute_url(),
            reverse(
                "events:EventDetail", args=[self.event.start_time.year, self.event.slug]
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
            start_time=make_aware(datetime(self.event.start_time.year, 1, 1)),
        )
        self.assertNotEqual(self.event.slug, event_same_year.slug)

    def test_events_with_different_years_can_have_equal_slugs(self):
        """Should allow events with different years to have equal slugs."""
        event_different_year = EventFactory(
            title=self.event.title,
            start_time=make_aware(datetime(1900, 1, 1)),
        )
        self.assertEqual(self.event.slug, event_different_year.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        event = EventFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(event.slug, slug)

    def test_start_time_defaults_to_now(self):
        """`start_time` should default to the current date and time."""
        self.assertAlmostEqual(self.event.start_time, now(), delta=timedelta(seconds=1))


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


class GetterTestCase(TestCase):
    def setUp(self):
        self.event = EventFactory()
        self.attendance = EventAttendanceFactory()

    def test_get_event_returns_event_if_it_exists(self):
        """Should return the event if it exists."""
        event = get_event_or_404(self.event.start_time.year, self.event.slug)
        self.assertEqual(self.event, event)

    def test_get_event_raises_404_if_event_not_exist(self):
        """Should raise 404 if event doesn't exist."""
        with self.assertRaises(Http404):
            get_event_or_404(1913, "not-exist")

    def test_get_attendance_returns_attendance_if_it_exists(self):
        """Should return the attendance if it exists."""
        attendance = get_event_attendance_or_404(
            self.attendance.event.start_time.year,
            self.attendance.event.slug,
            self.attendance.person.slug,
        )
        self.assertEqual(self.attendance, attendance)

    def test_get_attendance_raises_404_if_attendance_not_exist(self):
        """Should raise 404 if attendance doesn't exist."""
        with self.assertRaises(Http404):
            get_event_attendance_or_404(1913, "not-exist", "also-not-exist")


class EventBreadcrumbsTestSuite(TestMixin, TestCase):
    def test_normal(self):
        """Calling without arguments should give a single breadcrumb to EventList."""
        self.assertEqual(
            event_breadcrumbs(),
            [{"url": reverse("events:EventList"), "name": "Alle hendingar"}],
        )

    def test_year(self):
        """
        Calling with only a `year` argument should give 2 breadcrumbs to EventList and the
        EventList for that year.
        """
        self.assertEqual(
            event_breadcrumbs(year=2022),
            [
                {
                    "url": reverse("events:EventList"),
                    "name": "Alle hendingar",
                },
                {
                    "url": reverse("events:EventList", args=[2022]),
                    "name": "2022",
                },
            ],
        )

    def test_event(self):
        """
        Calling with an `event` argument should give 3 breadcrumbs to EventList, the
        EventList for that year and EventDetail.
        """
        event = EventFactory()
        self.assertEqual(
            event_breadcrumbs(event=event),
            [
                {
                    "url": reverse("events:EventList"),
                    "name": "Alle hendingar",
                },
                {
                    "url": reverse("events:EventList", args=[event.start_time.year]),
                    "name": str(event.start_time.year),
                },
                {
                    "url": reverse(
                        "events:EventDetail", args=[event.start_time.year, event.slug]
                    ),
                    "name": str(event),
                },
            ],
        )

    def test_event_and_year(self):
        """
        Calling with both a `year`and an `event` argument should make `event.start_time.year`
        override the given `year`.
        """
        event = EventFactory()
        self.assertEqual(
            event_breadcrumbs(year=event.start_time.year + 1, event=event),
            [
                {
                    "url": reverse("events:EventList"),
                    "name": "Alle hendingar",
                },
                {
                    "url": reverse("events:EventList", args=[event.start_time.year]),
                    "name": str(event.start_time.year),
                },
                {
                    "url": reverse(
                        "events:EventDetail", args=[event.start_time.year, event.slug]
                    ),
                    "name": str(event),
                },
            ],
        )


class EventListTestSuite(TestMixin, TestCase):
    def get_url(self, *args):
        return reverse("events:EventList", args=args)

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_attendance_form_in_context(self):
        """
        Create 3 events and check if they have attendance_form in their context.
        """
        [
            EventFactory(start_time=make_aware(datetime.now() + timedelta(1)))
            for _ in range(3)
        ]
        self.assertEqual(Event.objects.count(), 3)
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        events = response.context["events"]
        self.assertEqual(len(events), 3)
        for event in events:
            attendance_form = getattr(event, "attendance_form", None)
            self.assertIsNotNone(attendance_form)

    def test_event_feed_absolute_url_in_context(self):
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        event_feed_absolute_url = response.context["event_feed_absolute_url"]
        self.assertEquals(
            event_feed_absolute_url, "http://testserver/hendingar/taktlaushendingar.ics"
        )

    def test_filter_future_events(self):
        """
        Create 1 past and 1 future event and check if the number of events in context is correct.
        """
        EventFactory(start_time=make_aware(datetime.now() - timedelta(1)))
        EventFactory(start_time=make_aware(datetime.now() + timedelta(1)))
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEquals(len(response.context["events"]), 1)

    def test_filter_year_events(self):
        """
        Create different amount of events for 2020, 2021, 2022 and 2023 and check if the number of
        events in the contexts for the years are correct.
        """
        EventFactory(start_time=make_aware(datetime(2021, 1, 1)))
        EventFactory(start_time=make_aware(datetime(2022, 1, 1)))
        EventFactory(start_time=make_aware(datetime(2022, 2, 1)))
        EventFactory(start_time=make_aware(datetime(2023, 1, 1)))
        EventFactory(start_time=make_aware(datetime(2023, 2, 1)))
        EventFactory(start_time=make_aware(datetime(2023, 3, 1)))
        self.client.force_login(UserFactory())
        self.assertEquals(len(self.client.get(self.get_url(2020)).context["events"]), 0)
        self.assertEquals(len(self.client.get(self.get_url(2021)).context["events"]), 1)
        self.assertEquals(len(self.client.get(self.get_url(2022)).context["events"]), 2)
        self.assertEquals(len(self.client.get(self.get_url(2023)).context["events"]), 3)


class EventDetailTestCase(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        event = EventFactory()
        self.assertLoginRequired(
            reverse("events:EventDetail", args=[event.start_time.year, event.slug])
        )


class EventCreateTestCase(TestMixin, TestCase):
    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("events:EventCreate"))

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("events:EventCreate"),
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
    def setUp(self):
        self.event = EventFactory()
        self.event_data = {
            "title": "A Title",
            "start_time_0": "2021-11-25",
            "start_time_1": "16:30",
            "content": "Event text",
        }

    def get_url(self):
        """Returns the URL for the event update view for `event`."""
        return reverse(
            "events:EventUpdate", args=[self.event.start_time.year, self.event.slug]
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require the `change_event` permission."""
        self.assertPermissionRequired(
            self.get_url(),
            "events.change_event",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_event` permission.
        """
        self.client.force_login(self.event.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating event."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.event_data)

        created_by_previous = self.event.created_by
        self.event.refresh_from_db()
        self.assertEqual(self.event.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.event_data)

        self.event.refresh_from_db()
        self.assertEqual(self.event.modified_by, user)


class EventAttendanceListTestCase(TestMixin, TestCase):
    def get_url(self, event):
        """Returns the URL for the event attendance list view for `event`."""
        return reverse(
            "events:EventAttendanceList", args=[event.start_time.year, event.slug]
        )

    def setUp(self):
        self.event = EventFactory()

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
        return reverse(
            "events:EventAttendanceCreate", args=[event.start_time.year, event.slug]
        )

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


class EventAttendanceUpdateTestCase(TestMixin, TestCase):
    def get_url(self, attendance):
        """Returns the URL for the event attendance update view for `attendance`."""
        return reverse(
            "events:EventAttendanceUpdate",
            args=[
                attendance.event.start_time.year,
                attendance.event.slug,
                attendance.person.slug,
            ],
        )

    def setUp(self):
        self.user = UserFactory()
        self.attendance = EventAttendanceFactory(person=self.user)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.attendance))

    def test_requires_permission(self):
        """Should require the `change_eventattendance` permission."""
        self.assertPermissionRequired(
            self.get_url(self.attendance), "events.change_eventattendance"
        )

    def test_succeeds_if_not_permission_but_is_own(self):
        """
        Should succeed if it's the user's attendance,
        even if the user doesn't have the `change_eventattendance` permission.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.get_url(self.attendance))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class EventAttendanceDeleteTestCase(TestMixin, TestCase):
    def get_url(self, attendance):
        """Returns the URL for the event attendance delete view for `attendance`."""
        return reverse(
            "events:EventAttendanceDelete",
            args=[
                attendance.event.start_time.year,
                attendance.event.slug,
                attendance.person.slug,
            ],
        )

    def setUp(self):
        self.user = UserFactory()
        self.attendance = EventAttendanceFactory(person=self.user)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.attendance))

    def test_requires_permission(self):
        """Should require the `delete_eventattendance` permission."""
        self.assertPermissionRequired(
            self.get_url(self.attendance), "events.delete_eventattendance"
        )

    def test_succeeds_if_not_permission_but_is_own(self):
        """
        Should succeed if it's the user's attendance,
        even if the user doesn't have the `delete_eventattendance` permission.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.get_url(self.attendance))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_redirect_to_event_on_success(self):
        """Should redirect to the event on success."""
        self.client.force_login(self.user)
        response = self.client.post(self.get_url(self.attendance))
        self.assertRedirects(
            response,
            reverse(
                "events:EventDetail",
                args=[
                    self.attendance.event.start_time.year,
                    self.attendance.event.slug,
                ],
            ),
        )
