from django.conf import settings
from django.db.models import (
    CASCADE,
    RESTRICT,
    SET_NULL,
    CharField,
    ForeignKey,
    Model,
    TextChoices,
    TextField,
    UniqueConstraint,
    DateTimeField
)


class InstrumentGroup(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentgruppe"
        verbose_name_plural = "instrumentgrupper"
        ordering = ["name"]


class InstrumentType(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)
    group = ForeignKey(
        InstrumentGroup,
        verbose_name="instrumentgruppe",
        related_name="types",
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumenttype"
        verbose_name_plural = "instrumenttyper"
        ordering = ["name"]

    @classmethod
    def unknown(cls):
        group_unknown, created = InstrumentGroup.objects.get_or_create(name="Ukjend")
        type_unknown, created = InstrumentType.objects.get_or_create(
            name="Ukjend", defaults={"group": group_unknown}
        )
        return type_unknown


class InstrumentLocation(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentstad"
        verbose_name_plural = "instrumentstadar"


class Instrument(Model):
    type = ForeignKey(
        InstrumentType,
        verbose_name="instrumenttype",
        related_name="instruments",
        on_delete=RESTRICT,
    )
    identifier = CharField(max_length=255, verbose_name="identifikator", blank=True)
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

    last_modified = DateTimeField(auto_now=True, verbose_name="Sist endra")

    def get_state_order(self):
        ordering = ["GOOD", "OK", "BAD", "UNPLAYABLE"]
        return ordering.index(self.state)

    def __str__(self):
        return f"{self.type} {self.identifier}"

    class Meta:
        verbose_name = "instrument"
        verbose_name_plural = "instrument"
        ordering = ["type", "identifier"]
        constraints = [
            UniqueConstraint(fields=["type", "identifier"], name="unique_instrument")
        ]
