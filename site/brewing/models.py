from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    CheckConstraint,
    ForeignKey,
    IntegerField,
    Manager,
    Q,
    TextChoices,
)
from django.db.models.aggregates import Sum

from common.models import CreatedModifiedMixin


class Brew(CreatedModifiedMixin):
    name = CharField("namn", max_length=255, blank=True)
    price_per_litre = IntegerField("pris per liter")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "brygg"
        verbose_name_plural = "brygg"
        # Validate brew price larger than 0!


class TransactionManager(Manager):
    def sum(self):
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
    # Help text? Why is comment necessary? Mention that it isn't necessary?
    comment = CharField("kommentar", max_length=255, blank=True)
    type = CharField(
        "type",
        max_length=30,
        choices=TransactionType.choices,
    )

    def __str__(self):
        return f"{self.user} – {self.get_type_display()} – {self.price} NOK"

    class Meta:
        # ordering = ["name"]
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

    # Optional, required *for new* when transaction type is a purchase?
    # brew = ForeignKey()
