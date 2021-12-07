from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    Model,
    ForeignKey,
    IntegerChoices,
    DO_NOTHING,
)

from accounts.models import UserCustom


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
        on_delete=DO_NOTHING,
    )
    user = ForeignKey(
        UserCustom,
        verbose_name="vert lånt av",
        related_name="instruments",
        on_delete=DO_NOTHING,
        null=True,
        blank=True,
    )
    location = ForeignKey(
        InstrumentLocation,
        verbose_name="stad",
        related_name="instruments",
        on_delete=DO_NOTHING,
    )
    serial_number = CharField(max_length=255, verbose_name="serienummer", blank=True)
    comment = TextField(verbose_name="kommentar", blank=True)

    class State(IntegerChoices):
        GOOD = 0, "God"
        OK = 1, "Ok"
        BAD = 2, "Dårleg"
        UNPLAYABLE = 3, "Ikkje spelbart"

    state = IntegerField(
        verbose_name="tilstand",
        choices=State.choices,
        default=State.OK,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrument"
