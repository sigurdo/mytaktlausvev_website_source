from django.db.models import (
    CharField,
    TextField,
    Model,
    ForeignKey,
    TextChoices,
    DO_NOTHING,
)

from accounts.models import UserCustom


class InstrumentType(Model):
    name = CharField(max_length=255, verbose_name="namn")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentgruppe"
        verbose_name_plural = "instrumentgrupper"


class Instrument(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)
    type = ForeignKey(
        InstrumentType,
        verbose_name="instrumentgruppe",
        related_name="instruments",
        on_delete=DO_NOTHING,
        null=True,
        blank=True,
    )
    user = ForeignKey(
        UserCustom,
        verbose_name="vert lånt av",
        related_name="instruments",
        on_delete=DO_NOTHING,
        null=True,
        blank=True,
    )
    location = CharField(max_length=255, verbose_name="stad")
    serial_number = CharField(max_length=255, verbose_name="serienummer", blank=True)
    comment = TextField(verbose_name="kommentar", blank=True)

    class State(TextChoices):
        GOOD = "GOOD", "god"
        OK = "OK", "ok"
        BAD = "BAD", "dårleg"
        UNPLAYABLE = "UNPLAYABLE", "ikkje spelbart"

    state = CharField(
        max_length=255,
        verbose_name="tilstand",
        choices=State.choices,
        default=State.OK,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrument"
