from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from sheetmusic.factories import ScoreFactory

from .models import Repertoire, RepertoireEntry


class RepertoireFactory(DjangoModelFactory):
    class Meta:
        model = Repertoire

    name = "Repertoire"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class RepertoireEntryFactory(DjangoModelFactory):
    class Meta:
        model = RepertoireEntry

    repertoire = SubFactory(RepertoireFactory)
    score = SubFactory(ScoreFactory)
