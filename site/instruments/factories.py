from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from .models import Instrument, InstrumentGroup, InstrumentLocation


class InstrumentGroupFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentGroup

    name = sequence(lambda n: f"Instrumentgruppe #{n}")


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
