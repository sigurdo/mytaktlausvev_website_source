from django.conf import settings
from django.db.models import (
    RESTRICT,
    SET_NULL,
    CharField,
    ForeignKey,
    IntegerField,
    Model,
    TextChoices,
    TextField,
)


class JacketLocation(Model):
    name = CharField(max_length=255, verbose_name="namn")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jakkestad"
        verbose_name_plural = "jakkestadar"


class Jacket(Model):
    number = IntegerField(verbose_name="jakkenummer", unique=True)
    comment = TextField(verbose_name="kommentar", blank=True)

    class State(TextChoices):
        GOOD = "GOOD", "God"
        OK = "OK", "Ok"
        BAD = "BAD", "Dårleg"
        UNUSABLE = "UNUSABLE", "Ikkje brukbar"

    state = CharField(
        max_length=255,
        verbose_name="tilstand",
        choices=State.choices,
        default=State.OK,
    )

    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="eigar",
        related_name="owned_jackets",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )

    location = ForeignKey(
        JacketLocation,
        verbose_name="stad",
        related_name="jackets",
        on_delete=RESTRICT,
    )

    def get_state_order(self):
        ordering = ["GOOD", "OK", "BAD", "UNUSABLE"]
        return ordering.index(self.state)

    def __str__(self):
        return f"Jakke {self.number}"

    class Meta:
        verbose_name = "jakke"
        verbose_name_plural = "jakker"
