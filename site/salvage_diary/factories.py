from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Mascot, SalvageDiaryEntryExternal, SalvageDiaryEntryInternal


class MascotFactory(DjangoModelFactory):
    class Meta:
        model = Mascot

    name = "Berge Bergesen"

    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def creators(self, create, user_list):
        if not create or not user_list:
            return

        self.creators.set(user_list)


class SalvageDiaryEntryExternalFactory(DjangoModelFactory):
    class Meta:
        model = SalvageDiaryEntryExternal

    title = "Berging av Pandaen"
    thieves = "Juff-banden"
    mascot = SubFactory(MascotFactory)


class SalvageDiaryEntryInternalFactory(DjangoModelFactory):
    class Meta:
        model = SalvageDiaryEntryInternal

    title = "Berging av Pandaen"
    thieves = "Juff-banden"
    item = "Hans Harald"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def users(self, create, user_list):
        if not create or not user_list:
            return

        self.users.set(user_list)
