from django.db import models
from django.core import validators
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
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(getDefaultDeletedUser))
    calendar = models.ForeignKey(Julekalender, on_delete=models.CASCADE)
    index = models.IntegerField(
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(24)]
    )

    def windowExists(year, index):
        return Window.objects.filter(calendar=year, index=index).exists()

    def canEdit(self, user):
        return self.author == user

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["calendar", "index"], name="uniqueWindow")
        ]
