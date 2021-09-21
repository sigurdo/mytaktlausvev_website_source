"""Models for the quote-app"""

from django.db import models


class Quote(models.Model):
    """Model representing a single quote"""

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=2000)
    owner = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __str__(self):
        return self.text
