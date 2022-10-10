from django.conf import settings
from django.db.models import (
    RESTRICT,
    SET_NULL,
    CharField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextChoices,
    TextField,
)

from common.models import CreatedModifiedMixin


class JacketLocation(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jakkestad"
        verbose_name_plural = "jakkestadar"


class Jacket(CreatedModifiedMixin):
    number = IntegerField(verbose_name="jakkenummer", unique=True)
    comment = TextField(verbose_name="kommentar", blank=True)
    state_comment = TextField(verbose_name="tilstandskommentar", blank=True)

    class State(TextChoices):
        GOOD = "GOOD", "God"
        NEEDS_REPAIR = "NEEDS_REPAIR", "Treng reparasjon"
        UNUSABLE = "UNUSABLE", "Ikkje brukbar"

    state = CharField(
        max_length=255,
        verbose_name="tilstand",
        choices=State.choices,
        default=State.GOOD,
    )

    location = ForeignKey(
        JacketLocation,
        verbose_name="stad",
        related_name="jackets",
        on_delete=RESTRICT,
    )

    owner = OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="eigar",
        related_name="jacket",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    def get_state_order(self):
        ordering = ["GOOD", "NEEDS_REPAIR", "UNUSABLE"]
        return ordering.index(self.state)

    def __str__(self):
        return f"Jakke {self.number}"

    class Meta:
        ordering = ["number"]
        verbose_name = "jakke"
        verbose_name_plural = "jakker"
