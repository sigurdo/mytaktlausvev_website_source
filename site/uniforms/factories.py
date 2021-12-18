from factory import SubFactory, sequence
from factory.django import DjangoModelFactory

from .models import Jacket, JacketLocation




class JacketLocationFactory(DjangoModelFactory):
    class Meta:
        model = JacketLocation

    name = "Jakkeskapet"




class JacketFactory(DjangoModelFactory):
    class Meta:
        model = Jacket

    number = sequence(lambda n: 1 + n)
    owner = None
    location = SubFactory(JacketLocationFactory)
    comment = ""
    state = Jacket.State.OK


