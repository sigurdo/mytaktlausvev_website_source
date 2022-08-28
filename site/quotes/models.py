"""Models for the quote-app"""

from django.conf import settings
from django.db.models import CharField, ManyToManyField, TextField

from common.models import CreatedModifiedMixin


class Quote(CreatedModifiedMixin):
    """Model representing a single quote"""

    quote = TextField("sitat")
    quoted_as = CharField("sitert som", max_length=255, blank=True)
    users = ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="quotes",
        verbose_name="medlem som vert sitert",
        blank=True,
    )


    class Meta:
        ordering = ["-created"]
        verbose_name = "sitat"
        verbose_name_plural = "sitat"

    def __str__(self):
        stripped = self.quote.rstrip()
        if len(stripped) <= 25:
            return stripped
        return stripped[0:24] + "…"
