from datetime import datetime
from django.utils.timezone import make_aware
import factory
from accounts.factories import UserFactory
from .models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = "SMASH"
    content = "SMASH in Trondheim."
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    start_time = make_aware(datetime(2020, 11, 23, 12, 15, 00))
