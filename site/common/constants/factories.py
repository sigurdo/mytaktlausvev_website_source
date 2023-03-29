from factory import sequence
from factory.django import DjangoModelFactory

from .models import Constant


class ConstantFactory(DjangoModelFactory):
    class Meta:
        model = Constant

    name = sequence(lambda n: f"Konstant #{n}")
    value = "Konstant"
