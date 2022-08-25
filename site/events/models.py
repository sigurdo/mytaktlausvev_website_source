from datetime import datetime, timedelta

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    Manager,
    Model,
    TextChoices,
    UniqueConstraint,
)
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils.timezone import localtime, make_aware, now

from common.models import ArticleMixin


class EventCategory(Model):
    """Model representing an event category"""

    name = CharField(verbose_name="Namn", max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "hendingskategori"
        verbose_name_plural = "hendingskategoriar"


class EventManager(Manager):
    def upcoming(self):
        return super().filter(
            Q(end_time__gte=make_aware(datetime.now()))
            | Q(start_time__gte=make_aware(datetime.now() - timedelta(hours=12)))
        )


class Event(ArticleMixin):
    """Model representing an event."""

    objects = EventManager()
    start_time = DateTimeField("starttid", default=now)
    end_time = DateTimeField("sluttid", default=None, blank=True, null=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique_with="start_time__year",
        editable=True,
    )
    category = ForeignKey(
        EventCategory,
        on_delete=PROTECT,
        default=None,
        blank=False,
        null=True,
        verbose_name="Kategori",
        related_name="events",
    )

    def attending(self):
        return self.attendances.filter(status=Attendance.ATTENDING)

    def attending_maybe(self):
        return self.attendances.filter(status=Attendance.ATTENDING_MAYBE)

    def attending_not(self):
        return self.attendances.filter(status=Attendance.ATTENDING_NOT)

    def get_absolute_url(self):
        return reverse(
            "events:EventDetail", args=[localtime(self.start_time).year, self.slug]
        )

    def get_attendance(self, user):
        """
        Returns the EventAttendance for the given user on this event.
        Returns None if there is no EventAttendance registered for the user on this event.
        """
        return EventAttendance.objects.filter(person=user, event=self).first()

    def is_in_future(self):
        """Returns True if the event is in the future."""
        return self.start_time > make_aware(datetime.now())

    class Meta:
        ordering = ["start_time"]
        verbose_name = "hending"
        verbose_name_plural = "hendingar"


class Attendance(TextChoices):
    ATTENDING = "ATTENDING", "Deltek"
    ATTENDING_MAYBE = "ATTENDING_MAYBE", "Deltek kanskje"
    ATTENDING_NOT = "ATTENDING_NOT", "Deltek ikkje"


class EventAttendance(Model):
    """Model representing a registered attendance for an event."""

    event = ForeignKey(
        Event,
        on_delete=CASCADE,
        verbose_name="hending",
        related_name="attendances",
    )
    person = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name="person",
        related_name="event_attendances",
    )
    status = CharField("status", max_length=255, choices=Attendance.choices)

    created = DateTimeField("laga", auto_now_add=True)
    modified = DateTimeField("redigert", auto_now=True)

    def __str__(self):
        return f"{self.event} - {self.person} - {self.get_status_display()}"

    class Meta:
        verbose_name = "hendingdeltaking"
        verbose_name_plural = "hendingdeltakingar"
        ordering = ["person__date_joined"]
        constraints = [
            UniqueConstraint(fields=["event", "person"], name="unique_event_attendance")
        ]


class EventKeyinfoEntry(Model):
    """Model representing a keyinfo entry for an event."""

    key = CharField("nykel", max_length=255)
    info = CharField("info", max_length=1023, blank=True)
    order = FloatField(
        "rekkjefølgje",
        default=0,
        help_text="Definerer rekkjefølgja til oppføringar. Oppføringar med lik rekkjefølgje vert sortert etter nykel.",
    )
    event = ForeignKey(
        Event,
        on_delete=CASCADE,
        verbose_name="hending",
        related_name="keyinfo_entries",
    )

    def __str__(self):
        return f"{self.event} - {self.key}"

    class Meta:
        verbose_name = "Nykelinfo-oppføring for hending"
        verbose_name_plural = "Nykelinfo-oppføringar for hending"
        ordering = ["order", "key"]
        constraints = [
            UniqueConstraint(fields=["key", "event"], name="unique_EventKeyinfoEntry"),
        ]
