from datetime import datetime, timedelta
from http import HTTPStatus
from secrets import token_urlsafe

from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import make_aware, now

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data
from events.models import (
    Attendance,
    Event,
    EventAttendance,
    EventCategory,
    EventKeyinfoEntry,
)
from events.views import EventFeed, get_event_attendance_or_404, get_event_or_404
from instruments.factories import InstrumentTypeFactory

from .factories import (
    EventAttendanceFactory,
    EventCategoryFactory,
    EventFactory,
    EventKeyinfoEntryFactory,
)
from .forms import EventKeyinfoEntryFormset


class EventCategoryTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.category = EventCategoryFactory()

    def test_to_str(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            EventCategoryFactory(name=self.category.name)

    def test_ordering(self):
        """Should be ordered by `name`."""
        self.assertModelOrdering(
            EventCategory,
            EventCategoryFactory,
            [
                {"name": "AAA"},
                {"name": "BBB"},
                {"name": "ZZZ"},
            ],
        )


class EventManagerTestSuite(TestCase):
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


class EventTestSuite(TestCase):
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

    def test_cannot_delete_category_with_event(self):
        with self.assertRaises(ProtectedError):
            self.event.category.delete()

    def test_can_set_map_link_with_location(self):
        EventFactory(location="some place", location_map_link="https://some.link/")

    def test_cannot_set_map_link_without_location(self):
        with self.assertRaises(IntegrityError):
            EventFactory(location="", location_map_link="https://some.link/")

    def test_can_set_location_without_map_link(self):
        EventFactory(location="some place", location_map_link="")

    def test_can_set_neither_location_nor_map_link(self):
        EventFactory(location="", location_map_link="")

    def test_include_active_repertoires_defaults_to_false(self):
        event = EventFactory()
        self.assertFalse(event.include_active_repertoires)


class EventAttendanceTestSuite(TestCase):
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
        self.assertIn(self.attendance.person.get_preferred_name(), str(self.attendance))

    def test_to_str_includes_status(self):
        """`__str__` should include the status."""
        self.assertIn(self.attendance.get_status_display(), str(self.attendance))

    def test_instrument_group_returns_group_if_registered(self):
        """
        `instrument_group` should return the instrument group
        if an instrument type has been registered.
        """
        instrument_type = InstrumentTypeFactory()
        attendance = EventAttendanceFactory(instrument_type=instrument_type)
        self.assertEqual(attendance.instrument_group(), instrument_type.group)

    def test_instrument_group_returns_users_group_if_group_not_registered(self):
        """
        `instrument_group` should return the user's instrument group
        if an instrument type hasn't been registered, and the user has an instrument type.
        """
        user = UserFactory(instrument_type=InstrumentTypeFactory())
        attendance = EventAttendanceFactory(person=user, instrument_type=None)
        self.assertEqual(attendance.instrument_group(), user.instrument_type.group)

    def test_instrument_group_returns_none_if_no_instrument_type(self):
        """
        `instrument_group` should return `None`
        if neither the attendance nor the user has an instrument type.
        """
        user = UserFactory(instrument_type=None)
        attendance = EventAttendanceFactory(person=user, instrument_type=None)
        self.assertIsNone(attendance.instrument_group())


class EventKeyinfoEntryTestSuite(TestMixin, TestCase):
    def test_to_str(self):
        """str() should return "`event.title` - `key`"."""
        keyinfo = EventKeyinfoEntryFactory(event__title="SMASH", key="Price")
        self.assertEqual(str(keyinfo), "SMASH - Price")

    def test_delete_event_deletes_keyinfo(self):
        """Deleting event should delete related keyinfo entries."""
        keyinfo = EventKeyinfoEntryFactory()
        self.assertEqual(EventKeyinfoEntry.objects.count(), 1)
        keyinfo.event.delete()
        self.assertEqual(EventKeyinfoEntry.objects.count(), 0)

    def test_key_unique_for_same_event(self):
        """Different keyinfo entries cannot have same key for same event."""
        keyinfo = EventKeyinfoEntryFactory()
        with self.assertRaises(IntegrityError):
            EventKeyinfoEntryFactory(event=keyinfo.event, key=keyinfo.key)

    def test_same_key_for_other_event(self):
        """Different keyinfo entries can have same key for different events."""
        keyinfo = EventKeyinfoEntryFactory()
        EventKeyinfoEntryFactory(key=keyinfo.key)

    def test_ordering(self):
        """`EventKeyinfoEntry`s should be ordered first by order and then by key."""
        self.assertModelOrdering(
            EventKeyinfoEntry,
            EventKeyinfoEntryFactory,
            [
                {"order": 0, "key": "b"},
                {"order": 0, "key": "c"},
                {"order": 1, "key": "a"},
                {"order": 4.5, "key": "4.5"},
            ],
        )


class GetterTestSuite(TestCase):
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


class EventListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("events:EventList")

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

    def test_filter_future_events(self):
        """
        Create 1 past and 1 future event and check if the number of events in context is correct.
        """
        EventFactory(start_time=make_aware(datetime.now() - timedelta(1)))
        EventFactory(start_time=make_aware(datetime.now() + timedelta(1)))
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEquals(len(response.context["events"]), 1)


class EventListYearTestSuite(TestMixin, TestCase):
    def get_url(self, *args):
        return reverse("events:EventListYear", args=args)

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


class EventDetailTestSuite(TestMixin, TestCase):
    def get_url(self, event):
        return reverse("events:EventDetail", args=[event.start_time.year, event.slug])

    def test_requires_login(self):
        """Should require login."""
        event = EventFactory()
        self.assertLoginRequired(self.get_url(event))


class EventCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.category = EventCategoryFactory()

    def get_url(self):
        return reverse("events:EventCreate")

    def create_formset_post_data(self, data=[], total_forms=0, initial_forms=0):
        return create_formset_post_data(
            EventKeyinfoEntryFormset,
            data=data,
            total_forms=total_forms,
            initial_forms=initial_forms,
        )

    def create_required_form_data(self, include_formset=True):
        form_data = {
            "title": "A Title",
            "category": self.category.pk,
            "start_time_0": "2021-11-25",
            "start_time_1": "16:30",
            "content": "Event text",
        }
        if include_formset:
            form_data.update({**self.create_formset_post_data()})
        return form_data

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_can_set_fields_on_model(self):
        """Robustness test. You should be able to set model fields through form."""
        form_data = self.create_required_form_data()
        form_data["start_time_0"] = "2030-1-2"
        form_data["start_time_1"] = "20:30"
        form_data["end_time_0"] = "2030-1-2"
        form_data["end_time_1"] = "20:32"
        form_data["location"] = "A place"
        form_data["location_map_link"] = "https://a.place.no/"
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), form_data)
        event = Event.objects.last()
        self.assertEqual(event.start_time, make_aware(datetime(2030, 1, 2, 20, 30)))
        self.assertEqual(event.end_time, make_aware(datetime(2030, 1, 2, 20, 32)))
        self.assertEqual(event.location, form_data["location"])
        self.assertEqual(event.location_map_link, form_data["location_map_link"])

    def test_keyinfo(self):
        """Should be able to create keyinfo correctly."""
        form_data = self.create_required_form_data(include_formset=False)
        form_data.update(
            {
                **self.create_formset_post_data(
                    data=[
                        {"key": "Price", "info": "100kr", "order": 3},
                    ],
                    total_forms=1,
                    initial_forms=0,
                ),
            }
        )
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), form_data)
        self.assertEqual(EventKeyinfoEntry.objects.count(), 1)
        keyinfo = EventKeyinfoEntry.objects.last()
        self.assertEqual(keyinfo.key, "Price")
        self.assertEqual(keyinfo.info, "100kr")
        self.assertEqual(keyinfo.order, 3)


class EventUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.category = EventCategoryFactory()
        self.event = EventFactory(category=self.category)
        self.event_data = {
            "title": "A Title",
            "category": self.category.pk,
            "start_time_0": "2021-11-25",
            "start_time_1": "16:30",
            "content": "Event text",
            **self.create_formset_post_data(),
        }

    def create_formset_post_data(self, data=[], total_forms=0, initial_forms=0):
        return create_formset_post_data(
            EventKeyinfoEntryFormset,
            data=data,
            total_forms=total_forms,
            initial_forms=initial_forms,
        )

    def create_required_form_data(self, include_formset=True):
        form_data = {
            "title": "A Title",
            "category": self.category.pk,
            "start_time_0": "2021-11-25",
            "start_time_1": "16:30",
            "content": "Event text",
        }
        if include_formset:
            form_data.update({**self.create_formset_post_data()})
        return form_data

    def get_url(self, event=None):
        """Returns the URL for the event update view for `event`."""
        event = event or self.event
        return reverse("events:EventUpdate", args=[event.start_time.year, event.slug])

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

    def test_keyinfo(self):
        """Should be able to create keyinfo correctly."""
        form_data = self.create_required_form_data(include_formset=False)
        form_data.update(
            {
                **self.create_formset_post_data(
                    data=[
                        {"key": "Price", "info": "100kr", "order": 3},
                    ],
                    total_forms=1,
                    initial_forms=0,
                ),
            }
        )
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), form_data)
        self.assertEqual(EventKeyinfoEntry.objects.count(), 1)
        keyinfo = EventKeyinfoEntry.objects.last()
        self.assertEqual(keyinfo.key, "Price")
        self.assertEqual(keyinfo.info, "100kr")
        self.assertEqual(keyinfo.order, 3)


class EventDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.event = EventFactory()

    def get_url(self, event=None):
        event = event or self.event
        return reverse("events:EventDelete", args=[event.start_time.year, event.slug])

    def test_should_redirect_to_event_list_on_success(self):
        """Should redirect to the event list on success."""
        self.client.force_login(self.event.created_by)
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("events:EventList"))

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to delete events."""
        self.assertPermissionRequired(
            self.get_url(),
            "events.delete_event",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete events.
        """
        self.client.force_login(self.event.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_succeed_when_two_events_have_equal_slugs(self):
        """
        Should succeed even if two events have equal slugs,
        by utilizing the event's year.
        """
        self.event_same_slug = EventFactory(
            slug=self.event.slug, start_time=self.event.start_time + timedelta(days=400)
        )
        self.assertEqual(self.event.slug, self.event_same_slug.slug)

        self.client.post(self.get_url())
        Event.objects.get(pk=self.event.pk)


class EventAttendanceListTestSuite(TestMixin, TestCase):
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


class EventAttendanceCreateTestSuite(TestMixin, TestCase):
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


class EventAttendanceUpdateTestSuite(TestMixin, TestCase):
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


class EventAttendanceDeleteTestSuite(TestMixin, TestCase):
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


class EventFeedTestSuite(TestMixin, TestCase):
    def get_url(self, token=None):
        """Returns the URL for the event feed."""
        url = reverse(
            "events:EventFeed",
        )
        if token is not None:
            url += f"?token={token}"
        return url

    def test_no_token(self):
        """Accessing the event feed without a token should return 403."""
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_wrong_token(self):
        """Accessing the event feed with a wrong token should return 403."""
        token = token_urlsafe()
        response = self.client.get(self.get_url(token))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_correct_token(self):
        """Accessing the event feed with a correct token should return 200."""
        token = UserFactory().calendar_feed_token
        response = self.client.get(self.get_url(token))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_end_time_is_start_time_if_not_specified(self):
        """If event has no end time, the start time should be used."""
        event = EventFactory(end_time=None)
        end_time = EventFeed().item_end_datetime(event)
        self.assertEqual(end_time, event.start_time)

    def test_location(self):
        """calling `.item_location()` should return the event's location."""
        event = EventFactory(location="Gløs")
        location = EventFeed().item_location(event)
        self.assertEqual(location, "Gløs")
