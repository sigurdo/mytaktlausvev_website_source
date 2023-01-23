from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    Manager,
    TextChoices,
)
from django.db.models.aggregates import Sum

from common.models import CreatedModifiedMixin

# class Brew(CreatedModifiedMixin):
#     name = CharField("namn", max_length=255, blank=True)
#     price_per_litre = IntegerField(
#         "pris per liter",
#         validators=[MinValueValidator(0)],
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ["name"]
#         verbose_name = "brygg"
#         verbose_name_plural = "brygg"


class TransactionManager(Manager):
    def sum(self):
        return self.aggregate(sum=Sum("price"))["sum"] or 0


class Transaction(CreatedModifiedMixin):
    objects = TransactionManager()

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=CASCADE,
        related_name="brewing_transactions",
    )
    # Require positive/negative depending on type!
    price = IntegerField("pris")
    # Help text? Why is comment necessary?
    comment = CharField("kommentar", max_length=255, blank=True)

    class TransactionType(TextChoices):
        PURCHASE = "PURCHASE", "Kjøp"
        DEPOSIT = "DEPOSIT", "Innbetaling"

    type = CharField(
        "medlemsstatus",
        max_length=30,
        choices=TransactionType.choices,
    )

    def __str__(self):
        return f"{self.user} – {self.get_type_display()} – {self.price} NOK"

    class Meta:
        # ordering = ["name"]
        verbose_name = "transaksjon"
        verbose_name_plural = "transaksjonar"

    # Optional, required *for new* when transaction type is a purchase?
    # brew = ForeignKey()
