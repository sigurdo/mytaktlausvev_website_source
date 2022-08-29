"""Models for the quote-app"""

from django.conf import settings
from django.db.models import CharField, ManyToManyField, TextField

from common.models import CreatedModifiedMixin
from common.utils import comma_seperate_list


class Quote(CreatedModifiedMixin):
    """Model representing a single quote"""

    quote = TextField("sitat")
    quoted_as = CharField(
        "sitert som (med eventuell kontekst)", max_length=255, blank=True
    )
    users = ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="quotes",
        verbose_name="medlem som vert sitert",
        blank=True,
    )

    def quoted_as_or_users(self):
        return (
            self.quoted_as
            if self.quoted_as
            else comma_seperate_list([user.get_name() for user in self.users.all()])
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
