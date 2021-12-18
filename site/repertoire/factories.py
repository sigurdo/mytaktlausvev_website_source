from factory import SubFactory
from factory.django import DjangoModelFactory

from sheetmusic.factories import ScoreFactory

from .models import Repertoire, RepertoireEntry


class RepertoireFactory(DjangoModelFactory):
    class Meta:
        model = Repertoire

    name = "Repertoire"


class RepertoireEntryFactory(DjangoModelFactory):
    class Meta:
        model = RepertoireEntry

    repertoire = SubFactory(RepertoireFactory)
    score = SubFactory(ScoreFactory)
