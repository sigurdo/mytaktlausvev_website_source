from django.utils.timezone import now
from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Attendance, Event, EventAttendance, EventCategory, EventKeyinfoEntry


class EventCategoryFactory(DjangoModelFactory):
    class Meta:
        model = EventCategory

    name = sequence(lambda n: f"Category #{n}")


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = "SMASH"
    content = "SMASH in Trondheim."
    created_by = SubFactory(UserFactory)
    created = now()
    modified_by = SubFactory(UserFactory)
    modified = now()
    category = SubFactory(EventCategoryFactory)


class EventAttendanceFactory(DjangoModelFactory):
    class Meta:
        model = EventAttendance

    event = SubFactory(EventFactory)
    person = SubFactory(UserFactory)
    status = Attendance.ATTENDING


class EventKeyinfoEntryFactory(DjangoModelFactory):
    class Meta:
        model = EventKeyinfoEntry

    key = sequence(lambda n: f"Key #{n}")
    event = SubFactory(EventFactory)
