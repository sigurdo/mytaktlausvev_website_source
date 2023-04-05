from autoslug.fields import AutoSlugField
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    CheckConstraint,
    DateField,
    DateTimeField,
    F,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    Q,
    TextField,
)
from django.urls import reverse
from django.utils.timezone import now

from common.models import CreatedModifiedMixin
from common.utils import comma_seperate_list
from events.models import Event


class Mascot(CreatedModifiedMixin):
    name = CharField("namn", max_length=255)
    image = ImageField("bilete", upload_to="salvage_diary/mascots/", blank=True)
    creation_start_date = DateField(
        "startdato", blank=True, null=True, help_text="Når starta laginga av maskoten?"
    )
    creation_end_date = DateField(
        "sluttdato", blank=True, null=True, help_text="Når vert maskoten ferdig?"
    )
    password = CharField(
        "passord",
        max_length=255,
        blank=True,
        help_text="Dette er eit passord me festar på maskoten under hendinga som bergarne må fylla inn i skjemaet for å forsikra oss om at dei har berga maskoten.",
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
        verbose_name_plural = "maskotar"
        constraints = [
            CheckConstraint(
                check=(
                    Q(creation_end_date__gte=F("creation_start_date"))
                    | Q(creation_end_date__isnull=True)
                    | Q(creation_start_date__isnull=True)
                ),
                name="mascot_start_date_must_be_after_end_date",
                violation_error_message="""Så vidt me veit er tidsreiser enno ikkje offentleg tilgjengeleg, så startdatoen kan ikkje vera etter sluttdatoen. 
                Viss du kan reisa i tid, ver vennleg og gi beskjed til vevkom slik at me kan fjerna valideringa.""",
            )
        ]

    def __str__(self):
        return self.name

    def get_creators(self):
        return comma_seperate_list([user.get_name() for user in self.creators.all()])

    def get_url(self):
        return f"https://{Site.objects.get_current().domain}{reverse('salvage_diary:SalvageDiaryEntryExternalCreate', args=[self.slug])}"


class SalvageDiaryEntry(Model):
    title = CharField("tittel", max_length=255)
    thieves = CharField(
        "bergere", max_length=255, help_text="Kven er dykk?", blank=True
    )
    image = ImageField(
        "bilete",
        upload_to="salvage_diary/pictures",
        blank=True,
        help_text="Ønskjer du fleire bilete, lag fleire innlegg",
    )
    story = TextField(
        "Historie",
        blank=True,
        help_text="Kva skjedde? Korleis berga dykk den? Kva har dykk endra?",
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
    event = CharField(
        "hending",
        max_length=255,
        blank=True,
        help_text="Når skjedde dette? SMASH? TORSK? Medaljegalla?",
    )

    def item_or_mascot(self):
        return self.mascot

    def is_internal(self):
        return False

    class Meta:
        verbose_name = "bergedagbokinnlegg"
        verbose_name_plural = "bergedagbokinnlegg"


class SalvageDiaryEntryInternal(SalvageDiaryEntry, CreatedModifiedMixin):
    item = CharField("objekt", max_length=255, help_text="Kva ble berga?")
    event = ForeignKey(
        Event,
        on_delete=SET_NULL,
        verbose_name="hending",
        related_name="salvageDiaryEntries",
        null=True,
        blank=True,
    )
    users = ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="salvageDiaryEntries",
        verbose_name="involverte medlemmar",
        blank=True,
        help_text="Vel taktlause medlemmer som var involverte i berginga. Vil ikkje vises om 'Bergere' er fylt ut",
    )

    def item_or_mascot(self):
        return self.item

    def is_internal(self):
        return True

    def get_users(self):
        return comma_seperate_list([user.get_name() for user in self.users.all()])

    class Meta:
        verbose_name = "bergedagbokinnlegg - DT"
        verbose_name_plural = "bergedagbokinnlegg - DT"
