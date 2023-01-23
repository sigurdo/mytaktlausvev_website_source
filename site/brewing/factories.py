from factory import SubFactory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Transaction


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = SubFactory(UserFactory)
    price = 20
    type = Transaction.TransactionType.DEPOSIT
    created_by = SubFactory(UserFactory)
    modified_by = SubFactory(UserFactory)
