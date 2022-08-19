"""Models for the quote-app"""

from django.db import models

from common.models import CreatedModifiedMixin


class Quote(CreatedModifiedMixin):
    """Model representing a single quote"""

    quote = models.TextField("sitat")
    context = models.CharField("kontekst", max_length=255)

    class Meta:
        ordering = ["-created"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __str__(self):
        return self.quote
