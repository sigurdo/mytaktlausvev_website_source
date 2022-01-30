import factory

from accounts.factories import UserFactory

from .models import Attendance, Event, EventAttendance


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = "SMASH"
    content = "SMASH in Trondheim."
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class EventAttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventAttendance

    event = factory.SubFactory(EventFactory)
    person = factory.SubFactory(UserFactory)
    status = Attendance.ATTENDING
