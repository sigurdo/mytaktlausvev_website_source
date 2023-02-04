from math import ceil

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    Case,
    CharField,
    CheckConstraint,
    F,
    FloatField,
    ForeignKey,
    ImageField,
    IntegerField,
    Manager,
    Q,
    TextChoices,
    When,
)
from django.db.models.aggregates import Sum
from django.templatetags.static import static

from common.constants.models import Constant
from common.models import CreatedModifiedMixin


class Brew(CreatedModifiedMixin):
    name = CharField("namn", max_length=255, blank=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )
    price_per_liter = IntegerField("literpris", blank=True, null=True)
    available_for_purchase = BooleanField("tilgjengeleg for kjøp", default=False)
    OG = FloatField(
        "OG",
        blank=True,
        null=True,
        help_text="Original Gravity. Tettleiken av sukker i brygget før gjæring. Brukt for å berekne alkoholprosent.",
    )
    FG = FloatField(
        "FG",
        blank=True,
        null=True,
        help_text="Final Gravity. Tettleiken av sukker i brygget etter gjæring. Brukt for å berekne alkoholprosent.",
    )
    logo = ImageField("logo", upload_to="brewing/logos/", blank=True)

    def surcharge(self):
        """Returns the current surcharge for brews."""
        surcharge, _ = Constant.objects.get_or_create(
            name="Påslag på brygg i NOK", defaults={"value": "2"}
        )
        return int(surcharge.value)

    class Sizes(TextChoices):
        SIZE_0_33 = "SIZE_0_33", "0.33 L"
        SIZE_0_5 = "SIZE_0_5", "0.5 L"

    def price_per_0_33(self):
        """
        Returns the price for 0.33 L of the brew,
        rounded up to an integer.
        Returns None if the brew doesn't have a price per liter.
        """
        if not self.price_per_liter:
            return None
        return ceil(self.price_per_liter / 3) + self.surcharge()

    def price_per_0_5(self):
        """
        Returns the price for 0.5 L of the brew,
        rounded up to an integer.
        Returns None if the brew doesn't have a price per liter.
        """
        if not self.price_per_liter:
            return None
        return ceil(self.price_per_liter / 2) + self.surcharge()

    def alcohol_by_volume(self):
        """
        Calculates alcohol by volume (ABV) from OG and FG.
        Returns `None` if either OG or FG is missing.
        """
        if not self.OG or not self.FG:
            return None
        return (76.08 * (self.OG - self.FG) / (1.775 - self.OG)) * (self.FG / 0.794)

    def get_logo_url(self):
        """
        Returns a URL to the brew's logo if it exists,
        else the default logo.
        """
        if self.logo:
            return self.logo.url
        else:
            return static("brewing/default-brew-logo.svg")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        get_latest_by = "created"
        verbose_name = "brygg"
        verbose_name_plural = "brygg"
        constraints = [
            CheckConstraint(
                check=(Q(price_per_liter__gt=0) | Q(price_per_liter=None)),
                name="brew_price_per_liter_must_be_positive",
                violation_error_message="Literprisen til eit brygg må vere større enn 0.",
            ),
            CheckConstraint(
                check=(~Q(price_per_liter=None, available_for_purchase=True)),
                name="brew_price_required_if_available_for_purchase",
                violation_error_message="Literpris er påkravd om brygget skal vere tilgjengeleg for kjøp.",
            ),
        ]


class TransactionType(TextChoices):
    PURCHASE = "PURCHASE", "Kjøp"
    DEPOSIT = "DEPOSIT", "Innbetaling"


class TransactionManager(Manager):
    def balance(self):
        """
        Returns the balance of the manager's queryset, most commonly used to
        return a user's balance by calling `user.brewing_transactions.balance()`.
        """
        amount_sign_depending_on_type = Case(
            When(type=TransactionType.DEPOSIT, then=F("amount")),
            default=-F("amount"),
        )
        return (
            self.aggregate(balance=Sum(amount_sign_depending_on_type))["balance"] or 0
        )


class Transaction(CreatedModifiedMixin):
    objects = TransactionManager()

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=CASCADE,
        related_name="brewing_transactions",
    )
    amount = IntegerField("beløp")
    brew = ForeignKey(
        Brew,
        on_delete=SET_NULL,
        related_name="transactions",
        verbose_name="brygg",
        null=True,
        blank=True,
    )
    comment = CharField("kommentar", max_length=255, blank=True)
    type = CharField(
        "type",
        max_length=30,
        choices=TransactionType.choices,
    )

    def __str__(self):
        return f"{self.user} – {self.get_type_display()} – {self.amount} NOK"

    class Meta:
        ordering = ["-created"]
        get_latest_by = "created"
        verbose_name = "transaksjon"
        verbose_name_plural = "transaksjonar"
        constraints = [
            CheckConstraint(
                check=Q(amount__gt=0),
                name="transaction_amount_must_be_positive",
                violation_error_message="Beløpet til ein transaksjon må vere større enn 0.",
            )
        ]
