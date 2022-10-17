from factory import SubFactory, post_generation, sequence
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
    modified_by = SubFactory(UserFactory)
    category = SubFactory(EventCategoryFactory)

    @post_generation
    def repertoires(self, create, repertoire_list):
        if not create or not repertoire_list:
            return

        self.repertoires.set(repertoire_list)

    @post_generation
    def repertoire_extra_scores(self, create, repertoire_extra_scores_list):
        if not create or not repertoire_extra_scores_list:
            return

        self.repertoire_extra_scores.set(repertoire_extra_scores_list)


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
