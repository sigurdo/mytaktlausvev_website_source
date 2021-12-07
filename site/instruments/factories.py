from factory.django import DjangoModelFactory
from factory import SubFactory

from .models import InstrumentGroup, Instrument, InstrumentLocation


class InstrumentGroupFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentGroup

    name = "Instrumentgruppe"


class InstrumentLocationFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentLocation

    name = "Hovedskapet"


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
