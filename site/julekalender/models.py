from django.db import models


class Window(models.Model):
    """Model representing a window in a julekalender"""

    title = models.CharField(max_length=255)
    post = models.TextField()


class Julekalender(models.Model):
    """Model representing a year's julekalender"""

    year = models.IntegerField(primary_key=True)

    class Meta:
        ordering = ["-year"]


class Windows(models.Model):
    """Model holding the relationship between a year's julekalender and its windows"""

    year = models.ForeignKey(Julekalender, on_delete=models.CASCADE)
    window = models.ForeignKey(Window, on_delete=models.CASCADE)
    windowNumber = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["year", "windowNumber"], name="uniqueWindow"
            )
        ]
