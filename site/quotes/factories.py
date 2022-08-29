from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Quote


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    quote = "Det er farleg å gå åleine! Ta dette."
    quoted_as = "Gamal mann"
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)

    @post_generation
    def users(self, create, user_list):
        if not create or not user_list:
            return

        for user in user_list:
            self.users.add(user)
