from math import ceil

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    CheckConstraint,
    ForeignKey,
    IntegerField,
    Manager,
    Q,
    TextChoices,
)
from django.db.models.aggregates import Sum

from common.constants.models import Constant
from common.models import CreatedModifiedMixin


class Brew(CreatedModifiedMixin):
    name = CharField("namn", max_length=255, blank=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )
    price_per_liter = IntegerField("literpris", blank=True, null=True)
    # TODO: Available for purchase burde kunne overrides tå hendingo. Burde ha automatisk,
    # tegjængele, itte tegjængele. Tegjængele 1 time før, te 24 time ette?
    available_for_purchase = BooleanField("tilgjengeleg for kjøp", default=False)
    # TODO: Internt skjema for å kjøpe arbitrere øl for arbitrere folk. Berre folk me spesialtegang fer lov
    # TODO: OG and FG
    # TODO: Vis påslag?
    # TODO: Picture!

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
        return 0

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
                violation_error_message="Literprisen til eit brygg må vere positiv.",
            ),
            CheckConstraint(
                check=(~Q(price_per_liter=None, available_for_purchase=True)),
                name="brew_price_required_if_available_for_purchase",
                violation_error_message="Literpris er påkravd om brygget skal vere tilgjengeleg for kjøp.",
            ),
        ]


class TransactionManager(Manager):
    def balance(self):
        """Returns the balance of the queryset."""
        return self.aggregate(sum=Sum("price"))["sum"] or 0


class TransactionType(TextChoices):
    PURCHASE = "PURCHASE", "Kjøp"
    DEPOSIT = "DEPOSIT", "Innbetaling"


class Transaction(CreatedModifiedMixin):
    objects = TransactionManager()

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=CASCADE,
        related_name="brewing_transactions",
    )
    price = IntegerField("pris")
    # TODO: View that shows a history of your transactions
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
        return f"{self.user} – {self.get_type_display()} – {self.price} NOK"

    class Meta:
        ordering = ["-created"]
        get_latest_by = "created"
        verbose_name = "transaksjon"
        verbose_name_plural = "transaksjonar"
        constraints = [
            CheckConstraint(
                check=(
                    Q(type=TransactionType.DEPOSIT, price__gt=0)
                    | Q(type=TransactionType.PURCHASE, price__lt=0)
                ),
                name="brew_purchases_must_be_negative",
                violation_error_message="Innbetalingar må ha ein positiv pris, kjøp må ha ein negativ pris.",
            )
        ]
