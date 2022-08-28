"""Models for the quote-app"""

from django.db import models

from common.models import CreatedModifiedMixin


class Quote(CreatedModifiedMixin):
    """Model representing a single quote"""

    quote = models.TextField("sitat")
    quoted_as = models.CharField("sitert som", max_length=255)

    class Meta:
        ordering = ["-created"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __str__(self):
        stripped = self.quote.rstrip()
        if len(stripped) <= 25:
            return stripped
        return stripped[0:24] + "…"
