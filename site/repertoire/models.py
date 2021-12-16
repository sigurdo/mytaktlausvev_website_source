from io import BytesIO

from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    DateTimeField,
    CharField,
    Model,
)
from django.utils.text import slugify

from PyPDF2 import PdfFileReader, PdfFileWriter
from autoslug import AutoSlugField

from sheetmusic.models import Score, Part


class Repertoire(Model):
    """Model representing a repertoire"""

    name = CharField(max_length=255, verbose_name="namn")
    timestamp = DateTimeField(auto_now_add=True, verbose_name="tidsmerke")
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="name",
        unique=True,
        editable=True,
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["slug"], name="repertoire_unique_slug")]
        ordering = ["-timestamp"]
        verbose_name = "repertoar"
        verbose_name_plural = "repertoar"

    def __str__(self):
        return self.name

    def pdf_file(self, user):
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

    def pdf_filename(self, user):
        """Returns a nice filename for the PDF that contains the users favorite parts for this repertoire."""
        return slugify(f"{self.name} {user}") + ".pdf"


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
        verbose_name = "repertoaroppføring"
        verbose_name_plural = "repertoaroppføringar"

    def __str__(self):
        return f"{self.repertoire} - {self.score}"
