from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def getDefaultDeletedUser():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Julekalender(models.Model):
    """Model representing a year's julekalender"""

    year = models.IntegerField(primary_key=True)

    class Meta:
        ordering = ["-year"]


class Window(models.Model):
    """Model representing a window in a julekalender"""

    title = models.CharField(max_length=255)
    post = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(getDefaultDeletedUser))
    calendar = models.ForeignKey(Julekalender, on_delete=models.CASCADE)
    windowNumber = models.IntegerField()

    def windowExists(year, number):
        return Window.objects.filter(calendar=year, windowNumber=number).exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["calendar", "windowNumber"], name="uniqueWindow"
            )
        ]
