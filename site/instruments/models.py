from django.db.models import (
    CharField,
    TextField,
    TextChoices,
    Model,
    ForeignKey,
    SET_NULL,
    RESTRICT,
)
from django.conf import settings


class InstrumentGroup(Model):
    name = CharField(max_length=255, verbose_name="namn")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentgruppe"
        verbose_name_plural = "instrumentgrupper"


class InstrumentLocation(Model):
    name = CharField(max_length=255, verbose_name="namn")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentstad"
        verbose_name_plural = "instrumentstadar"


class Instrument(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)
    group = ForeignKey(
        InstrumentGroup,
        verbose_name="instrumentgruppe",
        related_name="instruments",
        on_delete=RESTRICT,
    )
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="vert lånt av",
        related_name="instruments",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    location = ForeignKey(
        InstrumentLocation,
        verbose_name="stad",
        related_name="instruments",
        on_delete=RESTRICT,
    )
    serial_number = CharField(max_length=255, verbose_name="serienummer", blank=True)
    comment = TextField(verbose_name="kommentar", blank=True)

    class State(TextChoices):
        GOOD = "GOOD", "God"
        OK = "OK", "Ok"
        BAD = "BAD", "Dårleg"
        UNPLAYABLE = "UNPLAYABLE", "Ikkje spelbart"

    state = CharField(
        max_length=255,
        verbose_name="tilstand",
        choices=State.choices,
        default=State.OK,
    )

    def get_state_order(self):
        ordering = ["GOOD", "OK", "BAD", "UNPLAYABLE"]
        return ordering.index(self.state)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrument"
