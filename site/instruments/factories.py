from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType


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

    name = "Instrument"
    group = SubFactory(InstrumentGroupFactory)
    user = None
    location = SubFactory(InstrumentLocationFactory)
    serial_number = "abc-123"
    comment = ""
    state = Instrument.State.OK
