from factory import SubFactory
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
