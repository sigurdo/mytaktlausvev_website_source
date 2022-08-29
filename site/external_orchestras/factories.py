from factory.django import DjangoModelFactory

from .models import Orchestra


class OrchestraFactory(DjangoModelFactory):
    class Meta:
        model = Orchestra

    name = "De Takløse"
    city = Orchestra.OrchestraCities.TRONDHEIM
