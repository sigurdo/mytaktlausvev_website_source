import io

from django.db.models import (
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    DateTimeField,
    CharField,
    Model,
)

from PyPDF2 import PdfFileReader, PdfFileWriter
from autoslug import AutoSlugField

import sheetmusic.models


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
        parts = []
        for entry in self.entries.all():
            for pdf in entry.score.pdfs.all():
                parts += pdf.parts.all()
        parts = list(filter(lambda part: part.is_favorite_for(user), parts))
        if len(parts) < 1:
            raise Exception(
                f"Fann inga favorittstemmer for {user} i repertoaret {self}"
            )
        pdf_writer = PdfFileWriter()
        for part in parts:
            pdf = PdfFileReader(part.pdf.file.path)
            for page_nr in range(part.from_page, part.to_page + 1):
                pdf_writer.addPage(pdf.getPage(page_nr - 1))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        return output_stream.getvalue()


class RepertoireEntry(Model):
    """Model representing a score entry in a repertoire"""

    repertoire = ForeignKey(Repertoire, on_delete=CASCADE, related_name="entries")
    score = ForeignKey(
        sheetmusic.models.Score,
        on_delete=CASCADE,
        related_name="repertoire_entries",
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
