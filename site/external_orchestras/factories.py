from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Orchestra

class OrchestraFactory(DjangoModelFactory):
    class Meta:
        model = Orchestra

    name = "De Takløse"
    city = Orchestra.OrchestraCities.TRONDHEIM