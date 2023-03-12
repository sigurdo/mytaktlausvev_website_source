from http import HTTPStatus

from django.db import IntegrityError
from django.templatetags.static import static
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from common.constants.factories import ConstantFactory
from common.mixins import TestMixin
from common.test_utils import test_image

from .factories import BrewFactory, TransactionFactory
from .models import Brew, Transaction, TransactionType


class BrewTestSuite(TestMixin, TestCase):
    def test_surcharge(self):
        """Returns the value of the surcharge constant, cast to an integer."""
        ConstantFactory(name="Påslag på brygg i NOK", value="5")
        brew = BrewFactory()
        self.assertEqual(brew.surcharge(), 5)

    def test_price_per_0_5(self):
        """Should return the price of the brew per 0.5 L, with the current surcharge."""
        ConstantFactory(name="Påslag på brygg i NOK", value="2")
        brew = BrewFactory(price_per_liter=20)
        self.assertEqual(brew.price_per_0_5(), 10 + 2)
        brew = BrewFactory(price_per_liter=15)
        self.assertEqual(brew.price_per_0_5(), 8 + 2)

    def test_price_per_0_5_returns_none_if_price_not_set(self):
        """Should return `None` if the price of the brew hasn't been set."""
        brew = BrewFactory(price_per_liter=None, available_for_purchase=False)
        self.assertIsNone(brew.price_per_0_5())

    def test_price_per_0_33(self):
        """Should return the price of the brew per 0.33 L, with the current surcharge."""
        ConstantFactory(name="Påslag på brygg i NOK", value="2")
        brew = BrewFactory(price_per_liter=9)
        self.assertEqual(brew.price_per_0_33(), 3 + 2)
        brew = BrewFactory(price_per_liter=10)
        self.assertEqual(brew.price_per_0_33(), 4 + 2)

    def test_price_per_0_33_returns_none_if_price_not_set(self):
        """Should return `None` if the price of the brew hasn't been set."""
        brew = BrewFactory(price_per_liter=None, available_for_purchase=False)
        self.assertIsNone(brew.price_per_0_33())

    def test_price_per_liter_must_be_positive(self):
        """Price per liter must be positive."""
        with self.assertRaises(IntegrityError):
            BrewFactory(price_per_liter=-5)

    def test_price_per_liter_required_to_be_available_for_purchase(self):
        """Price per liter should be required for the brew to be available for purchase."""
        with self.assertRaises(IntegrityError):
            BrewFactory(price_per_liter=None, available_for_purchase=True)

    def test_empty_brews_cannot_be_available_for_purchase(self):
        """Empty brews cannot be available for purchase."""
        with self.assertRaises(IntegrityError):
            BrewFactory(empty=True, available_for_purchase=True)

    def test_alcohol_by_volume(self):
        """Should return the ABV calculated from the OG and the FG."""
        brew = BrewFactory(OG=1.050, FG=1.010)
        self.assertAlmostEqual(brew.alcohol_by_volume(), 5.34, 2)
        brew = BrewFactory(OG=1.034, FG=1.002)
        self.assertAlmostEqual(brew.alcohol_by_volume(), 4.15, 2)
        brew = BrewFactory(OG=1.062, FG=0.992)
        self.assertAlmostEqual(brew.alcohol_by_volume(), 9.33, 2)

    def test_alcohol_by_volume_returns_none_if_missing_og_or_fg(self):
        """Should return `None` if either `OG` or `FG` is missing."""
        brew = BrewFactory(OG=None, FG=None)
        self.assertIsNone(brew.alcohol_by_volume())
        brew = BrewFactory(OG=1.050, FG=None)
        self.assertIsNone(brew.alcohol_by_volume())
        brew = BrewFactory(OG=None, FG=1.010)
        self.assertIsNone(brew.alcohol_by_volume())

    def test_get_logo_url_logo_exists(self):
        """
        `get_logo_url` should return the URL to
        the brew's logo when it exists.
        """
        brew = BrewFactory(logo=test_image())
        self.assertEqual(brew.get_logo_url(), brew.logo.url)

    def test_get_logo_url_logo_not_exist(self):
        """
        `get_logo_url` should return the default logo
        when the brew's logo doesn't exist.
        """
        brew = BrewFactory(logo="")
        self.assertEqual(brew.get_logo_url(), static("brewing/default-brew-logo.svg"))

    def test_empty_defaults_to_false(self):
        """A brew's emptiness should default to false."""
        self.assertFalse(BrewFactory().empty)

    def test_to_str(self):
        """`__str__` should be the brew's name."""
        brew = BrewFactory()
        self.assertEqual(str(brew), brew.name)


class TransactionTestSuite(TestMixin, TestCase):
    def test_to_str(self):
        """`__str__` should include user's name, the transaction type, and the amount."""
        transaction = TransactionFactory()
        self.assertIn(str(transaction.user), str(transaction))
        self.assertIn(transaction.get_type_display(), str(transaction))
        self.assertIn(str(transaction.amount), str(transaction))

    def test_balance(self):
        """Should return the sum of all transactions in the queryset, with deposits counted as negative."""
        user = UserFactory()
        for _ in range(3):
            TransactionFactory(user=user, amount=20, type=TransactionType.DEPOSIT)
            TransactionFactory(user=user, amount=10, type=TransactionType.PURCHASE)

        self.assertEqual(user.brewing_transactions.balance(), 30)

    def test_balance_returns_0_if_user_has_no_transactions(self):
        """Should return 0 if the user has no transactions."""
        user = UserFactory()
        self.assertIs(user.brewing_transactions.balance(), 0)

    def test_amount_must_be_positive(self):
        """The `amount` must be positive."""
        TransactionFactory(amount=20, type=TransactionType.DEPOSIT)
        TransactionFactory(amount=20, type=TransactionType.PURCHASE)
        with self.assertRaises(IntegrityError):
            TransactionFactory(amount=-20)


class BrewOverviewTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BrewOverview")

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_only_shows_available_brews(self):
        """Should only show brews that are available."""
        available_brew = BrewFactory(available_for_purchase=True)
        unavailable_brew = BrewFactory(available_for_purchase=False)

        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url())
        self.assertIn(available_brew, response.context["available_brews"])
        self.assertNotIn(unavailable_brew, response.context["available_brews"])


class BrewListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BrewList")

    def test_requires_permission_for_creating_brews(self):
        """Should require permission for creating brews."""
        self.assertLoginRequired(self.get_url())


class BrewCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BrewCreate")

    def test_requires_permission_for_creating_brews(self):
        """Should require permission for creating brews."""
        self.assertPermissionRequired(self.get_url(), "brewing.add_brew")

    def test_redirects_to_brew_list(self):
        """Should redirect to the brew list."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(), {"name": "Two Towers", "price_per_liter": 9}
        )
        self.assertRedirects(response, reverse("brewing:BrewList"))


class BrewUpdateTestSuite(TestMixin, TestCase):
    def setUp(self) -> None:
        self.brew = BrewFactory()

    def get_url(self):
        return reverse("brewing:BrewUpdate", args=[self.brew.slug])

    def test_requires_permission_for_creating_brews(self):
        """Should require permission for changing brews."""
        self.assertPermissionRequired(self.get_url(), "brewing.change_brew")

    def test_redirects_to_brew_list(self):
        """Should redirect to the brew list."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(
            self.get_url(), {"name": "Two Towers", "price_per_liter": 9}
        )
        self.assertRedirects(response, reverse("brewing:BrewList"))


class BalanceListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("brewing:BalanceList")

    def test_requires_permission_for_viewing_transactions(self):
        """Should require permission for viewing transactions."""
        self.assertPermissionRequired(self.get_url(), "brewing.view_transaction")

    def test_annotates_balance_purchased_deposited(self):
        """Should annotate users' balance, total purchased, and total deposited."""
        user = SuperUserFactory()
        TransactionFactory(amount=20, type=TransactionType.DEPOSIT, user=user)
        TransactionFactory(amount=20, type=TransactionType.DEPOSIT, user=user)
        TransactionFactory(amount=20, type=TransactionType.PURCHASE, user=user)

        self.client.force_login(user)
        response = self.client.get(self.get_url())

        user_in_response = response.context["users"].get(id=user.id)
        self.assertEqual(user_in_response.balance, 20)
        self.assertEqual(user_in_response.deposited, 40)
        self.assertEqual(user_in_response.purchased, 20)


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
        self.client.post(self.get_url(), {"amount": 20})

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.latest()
        self.assertEqual(deposit.user, user)
        self.assertEqual(deposit.type, TransactionType.DEPOSIT)

    def tests_ignores_changes_to_user_and_type(self):
        """Should ignore changes to the user and the transaction type."""
        logged_in_user = UserFactory()
        different_user = UserFactory()
        self.client.force_login(logged_in_user)
        self.client.post(
            self.get_url(),
            {"amount": 20, "user": different_user, "type": TransactionType.PURCHASE},
        )

        self.assertEqual(Transaction.objects.count(), 1)
        deposit = Transaction.objects.latest()
        self.assertEqual(deposit.user, logged_in_user)
        self.assertEqual(deposit.type, TransactionType.DEPOSIT)

    def test_rejects_amounts_0_or_smaller(self):
        """Should reject amounts that are 0 or smaller."""
        self.client.force_login(UserFactory())

        response = self.client.post(self.get_url(), {"amount": 0})
        self.assertFormError(
            response.context["form"],
            None,
            "Beløpet til ein transaksjon må vere større enn 0.",
        )

        response = self.client.post(self.get_url(), {"amount": -50})
        self.assertFormError(
            response.context["form"],
            None,
            "Beløpet til ein transaksjon må vere større enn 0.",
        )

    def test_increases_users_balance(self):
        """Should increase a user's balance."""
        user = UserFactory()
        self.assertEqual(user.brewing_transactions.balance(), 0)

        self.client.force_login(user)
        self.client.post(self.get_url(), {"amount": 20})
        self.assertEqual(user.brewing_transactions.balance(), 20)


class BrewPurchaseCreateTestSuite(TestMixin, TestCase):
    def get_url(self, brew, size=Brew.Sizes.SIZE_0_33):
        return f"{reverse('brewing:BrewPurchaseCreate', args=[brew.slug])}?size={size}"

    def setUp(self) -> None:
        self.brew = BrewFactory()

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url(self.brew))

    def test_sets_user_transaction_type_and_brew(self):
        """
        Should set the transaction `user` to the logged-in user,
        the transaction type to `PURCHASE`,
        and the brew to the current brew.
        """
        user = UserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(self.brew))

        self.assertEqual(Transaction.objects.count(), 1)
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.user, user)
        self.assertEqual(purchase.type, TransactionType.PURCHASE)
        self.assertEqual(purchase.brew, self.brew)

    def test_sets_brew_price_based_on_size(self):
        """Should set the transaction amount to the brew's price based on the size."""
        self.client.force_login(UserFactory())

        self.client.post(self.get_url(self.brew, Brew.Sizes.SIZE_0_33))
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.amount, self.brew.price_per_0_33())

        self.client.post(self.get_url(self.brew, Brew.Sizes.SIZE_0_5))
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.amount, self.brew.price_per_0_5())

    def test_size_0_33_by_default_and_if_size_invalid(self):
        """
        Should set the transaction amount to the brew's 0.33 L price
        if the size is missing or invalid.
        """
        self.client.force_login(UserFactory())

        self.client.post(self.get_url(self.brew, ""))
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.amount, self.brew.price_per_0_33())

        self.client.post(self.get_url(self.brew, "300 L"))
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.amount, self.brew.price_per_0_33())

    def tests_ignores_changes_to_user_type_amount_and_brew(self):
        """Should ignore changes to the user, transaction type, amount, and brew."""
        different_brew = BrewFactory()
        logged_in_user = UserFactory()
        different_user = UserFactory()
        self.client.force_login(logged_in_user)
        self.client.post(
            self.get_url(self.brew),
            {
                "amount": 20,
                "user": different_user,
                "type": TransactionType.DEPOSIT,
                "brew": different_brew,
            },
        )

        self.assertEqual(Transaction.objects.count(), 1)
        purchase = Transaction.objects.latest()
        self.assertEqual(purchase.user, logged_in_user)
        self.assertEqual(purchase.type, TransactionType.PURCHASE)
        self.assertEqual(purchase.amount, self.brew.price_per_0_33())
        self.assertEqual(purchase.brew, self.brew)

    def test_decreases_users_balance(self):
        """Should decrease a user's balance."""
        user = UserFactory()
        self.assertEqual(user.brewing_transactions.balance(), 0)

        self.client.force_login(user)
        self.client.post(self.get_url(self.brew))
        self.assertEqual(
            user.brewing_transactions.balance(), 0 - self.brew.price_per_0_33()
        )

    def test_returns_forbidden_for_unavailable_brews(self):
        """Should return `403 Forbidden` for unavailable brews."""
        self.client.force_login(SuperUserFactory())
        unavailable_brew = BrewFactory(available_for_purchase=False)

        response = self.client.get(self.get_url(unavailable_brew))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
