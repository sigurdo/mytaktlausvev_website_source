from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Repertoire


class RepertoireFactory(DjangoModelFactory):
    class Meta:
        model = Repertoire

    name = "Repertoire"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def scores(self, create, score_list):
        if not create or not score_list:
            return

        self.scores.set(score_list)
