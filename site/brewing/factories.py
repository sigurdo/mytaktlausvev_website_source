from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Brew, Transaction, TransactionType


class BrewFactory(DjangoModelFactory):
    class Meta:
        model = Brew

    name = "Gudbrandsdalsvatn"
    price_per_liter = 42
    available_for_purchase = True
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = SubFactory(UserFactory)
    amount = 20
    type = TransactionType.DEPOSIT
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
