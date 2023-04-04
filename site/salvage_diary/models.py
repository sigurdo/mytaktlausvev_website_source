from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    TextField,
)
from django.utils.timezone import now

from common.models import CreatedModifiedMixin
from common.utils import comma_seperate_list


class Mascot(CreatedModifiedMixin):
    name = CharField("namn", max_length=255)
    image = ImageField("bilete", upload_to="pictures/", blank=True)
    creationStartDate = DateField(
        "startdato", blank=True, null=True, help_text="Når starta laginga av maskoten?"
    )
    creationEndDate = DateField(
        "sluttdato", blank=True, null=True, help_text="Når ble maskoten ferdig?"
    )
    password = CharField(
        "passord",
        max_length=255,
        blank=True,
        help_text="Ein tekst streng som vi fester på maskoten under arrangement",
    )
    creators = ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Skapere",
    )

    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="name",
        unique=True,
        editable=True,
    )

    note = TextField(
        "Notat",
        blank=True,
    )

    class Meta:
        verbose_name = "maskot"
        verbose_name_plural = "maskoter"

    def __str__(self):
        return self.name

    def get_creators(self):
        return comma_seperate_list([user.get_name() for user in self.creators.all()])

    def get_creationStartDate(self):
        return self.creationStartDate or "?"

    def get_creationEndDate(self):
        return self.creationEndDate or "?"


class SalvageDiaryEntry(Model):
    title = CharField("titel", max_length=255)
    thieves = CharField("bergere", max_length=255, help_text="Kvem er dykk?")
    image = ImageField(
        "bilete",
        upload_to="salvage_diary/pictures",
        blank=True,
        help_text="Ønskar du fleir bilde, lag fleir innlegg",
    )
    story = TextField(
        "Historie",
        blank=True,
        help_text="Kva skjedde? Korleis berga dykk den? Kva har dykk endra?",
    )
    event = CharField(
        "hending",
        max_length=255,
        blank=True,
        help_text="Når skjedde dette? SMASH? TORSK? Medaljegalla?",
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class SalvageDiaryEntryExternal(SalvageDiaryEntry):
    created = DateTimeField("tidspunkt", default=now)
    mascot = ForeignKey(
        Mascot,
        on_delete=CASCADE,
        verbose_name="maskot",
        related_name="salvageEntries",
    )

    def get_item_or_mascot(self):
        return self.mascot

    def get_is_internal(self):
        return False

    class Meta:
        verbose_name = "bergedagbokinnlegg"
        verbose_name_plural = "bergedagbokinnlegg"


class SalvageDiaryEntryInternal(SalvageDiaryEntry, CreatedModifiedMixin):
    item = CharField("objekt", max_length=255, help_text="Kva ble berga?")

    def get_item_or_mascot(self):
        return self.item

    def get_is_internal(self):
        return True

    class Meta:
        verbose_name = "bergedagbokinnlegg - DT"
        verbose_name_plural = "bergedagbokinnlegg - DT"
