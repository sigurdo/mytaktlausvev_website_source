"""Models for the quote-app"""

from common.models import CreatedModifiedMixin
from django.db import models



class Quote(CreatedModifiedMixin):
    """Model representing a single quote"""

    text = models.CharField(max_length=2000)
    owner = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __str__(self):
        return self.text
