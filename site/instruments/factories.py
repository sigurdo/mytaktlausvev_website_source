from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType

from accounts.factories import UserFactory


class InstrumentGroupFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentGroup

    name = sequence(lambda n: f"Instrumentgruppe #{n}")


class InstrumentTypeFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentType

    name = sequence(lambda n: f"Instrumenttype #{n}")
    group = SubFactory(InstrumentGroupFactory)


class InstrumentLocationFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentLocation

    name = sequence(lambda n: f"Instrumentstad #{n}")


class InstrumentFactory(DjangoModelFactory):
    class Meta:
        model = Instrument

    type = SubFactory(InstrumentTypeFactory)
    identifier = sequence(lambda n: n)
    user = None
    location = SubFactory(InstrumentLocationFactory)
    serial_number = "abc-123"
    comment = ""
    state = Instrument.State.OK
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
