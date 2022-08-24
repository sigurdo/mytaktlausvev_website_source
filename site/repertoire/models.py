from io import BytesIO

from autoslug import AutoSlugField
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    Manager,
    Model,
    UniqueConstraint,
)
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from PyPDF2 import PdfFileReader, PdfFileWriter

from common.models import CreatedModifiedMixin
from sheetmusic.models import Part, Score


class RepertoireManager(Manager):
    def active(self):
        return super().filter(
            Q(active_until__isnull=True) | Q(active_until__gte=now().date())
        )


class Repertoire(CreatedModifiedMixin, Model):
    """Model representing a repertoire"""

    objects = RepertoireManager()
    name = CharField(max_length=255, verbose_name="namn")
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="name",
        unique=True,
        editable=True,
    )
    order = FloatField(
        verbose_name="rekkjefølgje",
        default=0,
        help_text=(
            "Definerer rekkjefølgja til repertoaret. "
            "Repertoar med lik rekkjefølgje vert sortert etter namn."
        ),
    )
    active_until = DateField(
        verbose_name="aktivt til",
        default=None,
        blank=True,
        null=True,
        help_text="Valfritt. Gjer repertoaret aktivt til og med ein bestemt dato. Om inga dato er satt vert det aktivt for alltid.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "repertoar"
        verbose_name_plural = "repertoar"

    def __str__(self):
        return self.name

    def is_active(self):
        return self.active_until is None or self.active_until >= now().date()

    def favorite_parts_pdf_file(self, user):
        """Returns a PDF contaning the user's favorite parts for the scores in this repertoire."""
        parts = Part.objects.filter(
            favoring_users__user=user, pdf__score__repertoire_entries__repertoire=self
        )
        if not parts.exists():
            raise Exception(
                f"Fann inga favorittstemmer for {user} i repertoaret {self}"
            )
        pdf_writer = PdfFileWriter()
        for entry in self.entries.all():
            try:
                pdf_writer.appendPagesFromReader(
                    PdfFileReader(entry.score.favorite_parts_pdf_file(user))
                )
            except:
                pass
        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def favorite_parts_pdf_filename(self, user):
        """Returns a nice filename for the PDF that contains the users favorite parts for this repertoire."""
        return slugify(f"{self.name} {user}") + ".pdf"

    def get_absolute_url(self):
        return reverse("repertoire:RepertoireDetail", args=[self.slug])


class RepertoireEntry(Model):
    """Model representing a score entry in a repertoire"""

    repertoire = ForeignKey(
        Repertoire,
        on_delete=CASCADE,
        related_name="entries",
        verbose_name="repertoar",
    )
    score = ForeignKey(
        Score,
        on_delete=CASCADE,
        related_name="repertoire_entries",
        verbose_name="note",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["repertoire", "score"], name="repertoire_unique_entry"
            )
        ]
        ordering = ["score"]
        verbose_name = "repertoaroppføring"
        verbose_name_plural = "repertoaroppføringar"

    def __str__(self):
        return f"{self.repertoire} - {self.score}"
