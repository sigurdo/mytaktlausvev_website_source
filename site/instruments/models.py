from django.conf import settings
from django.db.models import (
    CASCADE,
    RESTRICT,
    SET_NULL,
    CharField,
    ForeignKey,
    Manager,
    Model,
    TextChoices,
    TextField,
    UniqueConstraint,
)

from common.models import CreatedModifiedMixin


class InstrumentGroup(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentgruppe"
        verbose_name_plural = "instrumentgrupper"
        ordering = ["name"]


class InstrumentTypeManager(Manager):
    def sheatless_format(self):
        """Returns instrument types in a `Sheatless`-compatible format."""
        return {
            instrument_type.name: {
                "include": instrument_type.detection_keywords.values_list(
                    "keyword", flat=True
                ),
                "exceptions": instrument_type.detection_exceptions.values_list(
                    "exception", flat=True
                ),
            }
            for instrument_type in super().all()
        }


class InstrumentType(Model):
    objects = InstrumentTypeManager()

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


class InstrumentTypeDetectionKeyword(Model):
    keyword = CharField("nykelord", max_length=255, unique=True)
    instrument_type = ForeignKey(
        InstrumentType,
        verbose_name="instrumenttype",
        related_name="detection_keywords",
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = "instrumenttypeattkjenningsnykelord"
        verbose_name_plural = "instrumenttypeattkjenningsnykelord"
        ordering = ["keyword"]


class InstrumentTypeDetectionException(Model):
    exception = CharField("unntak", max_length=255)
    instrument_type = ForeignKey(
        InstrumentType,
        verbose_name="instrumenttype",
        related_name="detection_exceptions",
        on_delete=CASCADE,
    )

    def __str__(self):
        return self.exception

    class Meta:
        verbose_name = "instrumenttypeattkjenningsunntak"
        verbose_name_plural = "instrumenttypeattkjenningsunntak"
        ordering = ["exception"]
        constraints = [
            UniqueConstraint(
                fields=["exception", "instrument_type"],
                name="detection_exception_unique_for_instrument_type",
            )
        ]


class InstrumentLocation(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentstad"
        verbose_name_plural = "instrumentstadar"


class Instrument(CreatedModifiedMixin):
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
