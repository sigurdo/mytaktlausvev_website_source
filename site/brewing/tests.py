from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from common.mixins import TestMixin

from .factories import TransactionFactory
from .models import Transaction, TransactionType


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
            TransactionFactory(user=user, price=20, type=TransactionType.DEPOSIT)
            TransactionFactory(user=user, price=-10, type=TransactionType.PURCHASE)

        self.assertEqual(user.brewing_transactions.sum(), 30)

    def test_sum_returns_0_if_user_has_no_transactions(self):
        """Should return 0 if the user has no transactions."""
        user = UserFactory()
        self.assertIs(user.brewing_transactions.sum(), 0)

    def test_deposits_must_be_positive(self):
        """Deposits must have a positive price."""
        TransactionFactory(price=20, type=TransactionType.DEPOSIT)
        with self.assertRaises(IntegrityError):
            TransactionFactory(price=-20, type=TransactionType.DEPOSIT)

    def test_purchases_must_be_negative(self):
        """Purchases must have a negative price."""
        TransactionFactory(price=-20, type=TransactionType.PURCHASE)
        with self.assertRaises(IntegrityError):
            TransactionFactory(price=20, type=TransactionType.PURCHASE)


class DepositCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:DepositCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_sets_user_to_logged_in_user(self):
        """Should set the transaction `user` to the logged-in user."""
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), {"price": 20})

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.last()
        self.assertEqual(deposit.user, user)

    def test_sets_transaction_type_to_deposit(self):
        """Should set the transaction type to `DEPOSIT`."""
        self.client.force_login(UserFactory())
        self.client.post(self.get_url(), {"price": 20})

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.last()
        self.assertEqual(deposit.type, TransactionType.DEPOSIT)

    def tests_ignores_changes_to_user_and_type(self):
        """Should ignore changes to the user and the transaction type."""
        logged_in_user = UserFactory()
        different_user = UserFactory()
        self.client.force_login(logged_in_user)
        self.client.post(
            self.get_url(),
            {"price": 20, "user": different_user, "type": TransactionType.PURCHASE},
        )

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.last()
        self.assertEqual(deposit.user, logged_in_user)
        self.assertEqual(deposit.type, TransactionType.DEPOSIT)

    def test_rejects_prices_0_or_smaller(self):
        """Should reject prices that are 0 or smaller."""
        self.client.force_login(UserFactory())

        response = self.client.post(self.get_url(), {"price": 0})
        self.assertFormError(
            response.context["form"],
            None,
            "Innbetalingar må ha ein positiv pris, kjøp må ha ein negativ pris.",
        )

        response = self.client.post(self.get_url(), {"price": -50})
        self.assertFormError(
            response.context["form"],
            None,
            "Innbetalingar må ha ein positiv pris, kjøp må ha ein negativ pris.",
        )
