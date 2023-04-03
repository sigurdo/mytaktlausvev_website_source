from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Mascot, SalvageDiaryEntry


class MascotFactory(DjangoModelFactory):
    class Meta:
        model = Mascot

    name = "Berge Bergesen"
    slug = "berge"

    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def creators(self, create, user_list):
        if not create or not user_list:
            return

        self.creators.set(user_list)


class SalvageDiaryEntryFactory(DjangoModelFactory):
    class Meta:
        model = SalvageDiaryEntry

    title = "Berging av Pandaen"
    thieves = "Juff-banden"
    mascot = SubFactory(MascotFactory)
