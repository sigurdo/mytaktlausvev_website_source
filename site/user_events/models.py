from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    """Model representing an event"""
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=None, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def attendance_status(self):
        return EventAttendance.objects.filter(event=self)

    def attending(self):
        return [a.person for a in self.attendance_status().filter(status=Attendance.ATTENDING)]

    def not_attending(self):
        return [a.person for a in self.attendance_status().filter(status=Attendance.NOT_ATTENDING)]

    def might_be_attending(self):
        return [a.person for a in self.attendance_status().filter(status=Attendance.MIGHT_BE_ATTENDING)]

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title


class Attendance(models.IntegerChoices):
    NOT_ATTENDING = 0, _("Deltek ikkje")
    MIGHT_BE_ATTENDING = 1, _("Deltek kanskje")
    ATTENDING = 2, _("Deltek")


class EventAttendance(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=Attendance.choices)
