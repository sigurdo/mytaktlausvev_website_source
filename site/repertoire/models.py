from io import BytesIO

from autoslug import AutoSlugField
from django.db.models import (
    CharField,
    DateField,
    FloatField,
    Manager,
    ManyToManyField,
    Model,
)
from django.db.models.query_utils import Q
from django.urls import reverse
from django.utils.timezone import localdate, now
from PyPDF2 import PdfFileReader, PdfFileWriter

from common.models import CreatedModifiedMixin
from sheetmusic.models import Part, Score


class RepertoireManager(Manager):
    def active(self, date=None):
        date = date or localdate()
        return super().filter(
            (Q(active_until__isnull=True) | Q(active_until__gte=date))
            & Q(created__date__lte=date)
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
    scores = ManyToManyField(
        Score,
        related_name="repertoires",
        verbose_name="notar",
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
        """Returns a PDF containing the user's favorite parts for the scores in this repertoire."""
        parts = Part.objects.filter(
            favoring_users__user=user, pdf__score__repertoires=self
        )
        if not parts.exists():
            raise Exception(
                f"Fann inga favorittstemmer for {user} i repertoaret {self}"
            )
        pdf_writer = PdfFileWriter()
        for score in self.scores.all():
            try:
                pdf_writer.appendPagesFromReader(
                    PdfFileReader(score.favorite_parts_pdf_file(user))
                )
            except:
                pass
        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def favorite_parts_pdf_filename(self, user):
        """Returns a nice filename for the PDF that contains the user's favorite parts for this repertoire."""
        return f"{self.name} - {user}.pdf"

    def get_absolute_url(self):
        return reverse("repertoire:RepertoireDetail", args=[self.slug])
