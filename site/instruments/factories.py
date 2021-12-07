from factory.django import DjangoModelFactory

from .models import InstrumentType


class InstrumentTypeFactory(DjangoModelFactory):
    class Meta:
        model = InstrumentType

    name = "Instrumentgruppe"
