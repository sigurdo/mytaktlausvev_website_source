from factory import sequence
from factory.django import DjangoModelFactory

from .models import EmbeddableText


class EmbeddableTextFactory(DjangoModelFactory):
    class Meta:
        model = EmbeddableText

    name = sequence(lambda n: f"Text #{n}")
