from django.db import models


class Julekalender(models.Model):
    """Model representing a year's julekalender"""

    year = models.IntegerField(primary_key=True)

    class Meta:
        ordering = ["-year"]


class Window(models.Model):
    """Model representing a window in a julekalender"""

    title = models.CharField(max_length=255)
    post = models.TextField()
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
