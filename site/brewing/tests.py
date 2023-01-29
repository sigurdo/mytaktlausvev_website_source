from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from accounts.models import UserCustom
from common.constants.factories import ConstantFactory
from common.mixins import TestMixin

from .factories import BrewFactory, TransactionFactory
from .models import Brew, Transaction, TransactionType


class BrewTestSuite(TestMixin, TestCase):
    def test_surcharge(self):
        """Returns the value of the surcharge constant, cast to an integer."""

    def test_price_per_0_5(self):
        """Should return the price of the brew per 0.5 L, with the current surcharge."""
        ConstantFactory(name="Påslag på brygg i NOK", value="2")
        brew = BrewFactory(price_per_litre=20)
        self.assertEqual(brew.price_per_0_5(), 10 + 2)
        brew = BrewFactory(price_per_litre=15)
        self.assertEqual(brew.price_per_0_5(), 8 + 2)

    def test_price_per_0_33(self):
        """Should return the price of the brew per 0.33 L, with the current surcharge."""
        ConstantFactory(name="Påslag på brygg i NOK", value="2")
        brew = BrewFactory(price_per_litre=9)
        self.assertEqual(brew.price_per_0_33(), 3 + 2)
        brew = BrewFactory(price_per_litre=10)
        self.assertEqual(brew.price_per_0_33(), 4 + 2)

    def test_to_str(self):
        """`__str__` should be the brew's name."""
        brew = BrewFactory()
        self.assertEqual(str(brew), brew.name)


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

        self.assertEqual(user.brewing_transactions.balance(), 30)

    def test_sum_returns_0_if_user_has_no_transactions(self):
        """Should return 0 if the user has no transactions."""
        user = UserFactory()
        self.assertIs(user.brewing_transactions.balance(), 0)

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


class BrewCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BrewCreate")

    def test_requires_permission_for_creating_brews(self):
        """Should require permission for creating brews."""
        self.assertPermissionRequired(self.get_url(), "brewing.add_brew")


class BalanceListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BalanceList")

    def test_requires_permission_for_viewing_transactions(self):
        """Should require permission for viewing transactions."""
        self.assertPermissionRequired(self.get_url(), "brewing.view_transaction")

    def test_excludes_inactive_users(self):
        """Should exclude inactive users."""
        inactive = UserFactory(membership_status=UserCustom.MembershipStatus.INACTIVE)

        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url())

        self.assertNotIn(inactive, response.context["users"])

    def test_annotates_balance_purchased_deposited(self):
        """Should annotate users' balance, total purchased, and total deposited."""
        user = SuperUserFactory()
        TransactionFactory(price=20, type=TransactionType.DEPOSIT, user=user)
        TransactionFactory(price=20, type=TransactionType.DEPOSIT, user=user)
        TransactionFactory(price=-20, type=TransactionType.PURCHASE, user=user)

        self.client.force_login(user)
        response = self.client.get(self.get_url())

        user_in_response = response.context["users"].get(id=user.id)
        self.assertEqual(user_in_response.balance, 20)
        self.assertEqual(user_in_response.deposited, 40)
        self.assertEqual(user_in_response.purchased, -20)


class DepositCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:DepositCreate")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_sets_user_and_transaction_type(self):
        """
        Should set the transaction `user` to the logged-in user,
        and the transaction type to `DEPOSIT`.
        """
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), {"price": 20})

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.last()
        self.assertEqual(deposit.user, user)
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

    def test_increases_users_balance(self):
        """Should increase a user's balance."""
        user = UserFactory()
        self.assertEqual(user.brewing_transactions.balance(), 0)

        self.client.force_login(user)
        self.client.post(self.get_url(), {"price": 20})
        self.assertEqual(user.brewing_transactions.balance(), 20)


class BrewPurchaseCreateTestSuite(TestMixin, TestCase):
    def get_url(self, brew, size=Brew.Sizes.SIZE_0_33):
        return f"{reverse('brewing:BrewPurchaseCreate', args=[brew.pk])}?size={size}"

    def setUp(self) -> None:
        self.brew = BrewFactory()

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.brew))

    def test_sets_user_and_transaction_type(self):
        """
        Should set the transaction `user` to the logged-in user,
        and the transaction type to `PURCHASE`.
        """
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(self.brew))

        self.assertEqual(Transaction.objects.count(), 1)
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.user, user)
        self.assertEqual(purchase.type, TransactionType.PURCHASE)

    def test_sets_negative_brew_price_based_on_size(self):
        """Should set the transaction price to the brew's price based on the size, but negative."""
        self.client.force_login(UserFactory())

        self.client.post(self.get_url(self.brew, Brew.Sizes.SIZE_0_33))
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.price, -self.brew.price_per_0_33())

        self.client.post(self.get_url(self.brew, Brew.Sizes.SIZE_0_5))
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.price, -self.brew.price_per_0_5())

    def test_size_0_33_by_default_and_if_size_invalid(self):
        """
        Should set the transaction price to the brew's 0.33 L price (negative)
        if the size is missing or invalid.
        """
        self.client.force_login(UserFactory())

        self.client.post(self.get_url(self.brew, ""))
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.price, -self.brew.price_per_0_33())

        self.client.post(self.get_url(self.brew, "300 L"))
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.price, -self.brew.price_per_0_33())

    def tests_ignores_changes_to_user_type_and_price(self):
        """Should ignore changes to the user, transaction type, and price."""
        logged_in_user = UserFactory()
        different_user = UserFactory()
        self.client.force_login(logged_in_user)
        self.client.post(
            self.get_url(self.brew),
            {"price": 20, "user": different_user, "type": TransactionType.DEPOSIT},
        )

        self.assertEqual(Transaction.objects.count(), 1)
        purchase = Transaction.objects.last()
        self.assertEqual(purchase.user, logged_in_user)
        self.assertEqual(purchase.type, TransactionType.PURCHASE)
        self.assertEqual(purchase.price, -self.brew.price_per_0_33())

    def test_decreases_users_balance(self):
        """Should decrease a user's balance."""
        user = UserFactory()
        self.assertEqual(user.brewing_transactions.balance(), 0)

        self.client.force_login(user)
        self.client.post(self.get_url(self.brew))
        self.assertEqual(
            user.brewing_transactions.balance(), 0 - self.brew.price_per_0_33()
        )
