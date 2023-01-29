from math import ceil

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
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
    # TODO: Dev data! + navbar
    name = CharField("namn", max_length=255, blank=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )
    price_per_litre = IntegerField("literpris")
    # TODO: Available for purchase burde kunne overrides tå hendingo. Burde ha automatisk,
    # tegjængele, itte tegjængele. Tegjængele 1 time før, te 24 time ette?
    available_for_purchase = BooleanField("tilgjengeleg for kjøp", default=False)
    # TODO: Internt skjema for å kjøpe arbitrere øl for arbitrere folk. Berre folk me spesialtegang fer lov
    # TODO: OG and FG
    # TODO: Vis påslag?

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
        """
        return ceil(self.price_per_litre / 3) + self.surcharge()

    def price_per_0_5(self):
        """
        Returns the price for 0.5 L of the brew,
        rounded up to an integer.
        """
        return ceil(self.price_per_litre / 2) + self.surcharge()

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
        verbose_name = "brygg"
        verbose_name_plural = "brygg"
        # Validate brew price larger than 0!


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
    # TODO: Help text? Why is comment necessary? Mention that it isn't necessary?
    comment = CharField("kommentar", max_length=255, blank=True)
    type = CharField(
        "type",
        max_length=30,
        choices=TransactionType.choices,
    )

    def __str__(self):
        return f"{self.user} – {self.get_type_display()} – {self.price} NOK"

    class Meta:
        ordering = ["created"]
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

    # TODO: Optional, required *for new* when transaction type is a purchase?
    # brew = ForeignKey()
