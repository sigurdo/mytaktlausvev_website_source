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


class Mascot(CreatedModifiedMixin):
    name = CharField("namn", max_length=255)
    image = ImageField("bilete", upload_to="pictures/", blank=True)
    creationStartDate = DateField(
        "startdato", blank=True, help_text="Når starta laginga av maskoten?"
    )
    creationEndDate = DateField(
        "sluttdato", blank=True, help_text="Når ble maskoten ferdig?"
    )
    passord = CharField("passord", max_length=255, blank=True)
    creators = ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="creator",
    )

    class Meta:
        verbose_name = "maskot"
        verbose_name_plural = "maskoter"

    def __str__(self):
        return self.name


class SalvageDiaryEntry(Model):
    title = CharField("titel", max_length=255)
    time = DateTimeField("tidspunkt", default=now)
    thieves = CharField("bergere", max_length=255, help_text="Kvem er dykk?")
    mascot = ForeignKey(
        Mascot,
        on_delete=CASCADE,
        verbose_name="maskot",
        related_name="salvageEntries",
    )
    image = ImageField("bilete", upload_to="pictures/", blank=True)
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
        return self.mascot + " - " + self.title
    
    class Meta:
        verbose_name = "bergedagbokinnlegg"
        verbose_name_plural = "bergedagbokinnlegg"
