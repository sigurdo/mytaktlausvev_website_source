from factory.django import DjangoModelFactory

from .models import InstrumentGroup


class InstrumentGroupFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentGroup

    name = "Instrumentgruppe"
