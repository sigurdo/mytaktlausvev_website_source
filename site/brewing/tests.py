from django.test import TestCase

from accounts.factories import UserFactory
from common.mixins import TestMixin

from .factories import TransactionFactory
from .models import Transaction


class TransactionTestSuite(TestMixin, TestCase):
    def test_to_str(self):
        """`__str__` should include user's name, the transaction type, and the price."""
        transaction = TransactionFactory()
        self.assertIn(str(transaction.user), str(transaction))
        self.assertIn(transaction.get_type_display(), str(transaction))
        self.assertIn(str(transaction.price), str(transaction))

    def test_sum(self):
        """Should return the sum of all transactions in the queryset."""
        user = UserFactory()
        for _ in range(3):
            TransactionFactory(
                user=user, price=20, type=Transaction.TransactionType.DEPOSIT
            )
            TransactionFactory(
                user=user, price=-10, type=Transaction.TransactionType.PURCHASE
            )

        self.assertEqual(user.brewing_transactions.sum(), 30)

    def test_sum_returns_0_if_user_has_no_transactions(self):
        """Should return 0 if the user has no transactions."""
        user = UserFactory()
        self.assertIs(user.brewing_transactions.sum(), 0)
