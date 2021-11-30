from django.db import models
from django.conf import settings
from django.urls import reverse
from common.models import ArticleMixin
from autoslug.fields import AutoSlugField


class Event(ArticleMixin):
    """Model representing an event."""

    start_time = models.DateTimeField("starttid")
    end_time = models.DateTimeField("sluttid", default=None, blank=True, null=True)

    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique_with="start_time__year",
        editable=True,
    )

    def attending(self):
        return self.attendances.filter(status=Attendance.ATTENDING)

    def attending_maybe(self):
        return self.attendances.filter(status=Attendance.ATTENDING_MAYBE)

    def attending_not(self):
        return self.attendances.filter(status=Attendance.ATTENDING_NOT)

    def get_absolute_url(self):
        return reverse("events:EventDetail", args=[self.start_time.year, self.slug])

    class Meta:
        ordering = ["start_time"]
        verbose_name = "hending"
        verbose_name_plural = "hendingar"


class Attendance(models.TextChoices):
    ATTENDING = "ATTENDING", "Deltek"
    ATTENDING_MAYBE = "ATTENDING_MAYBE", "Deltek kanskje"
    ATTENDING_NOT = "ATTENDING_NOT", "Deltek ikkje"


class EventAttendance(models.Model):
    """Model representing a registered attendance for an event."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="hending",
        related_name="attendances",
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="person",
        related_name="event_attendances",
    )
    status = models.CharField("status", max_length=255, choices=Attendance.choices)

    created = models.DateTimeField("laga", auto_now_add=True)

    def __str__(self):
        return f"{self.event} - {self.person} - {self.get_status_display()}"

    class Meta:
        verbose_name = "hendingdeltaking"
        verbose_name_plural = "hendingdeltakingar"
        constraints = [
            models.UniqueConstraint(
                fields=["event", "person"], name="unique_event_attendance"
            )
        ]
