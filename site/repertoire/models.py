import io

from django.db import models

from PyPDF2 import PdfFileReader, PdfFileWriter

import sheetmusic.models


class Repertoire(models.Model):
    """Model representing a repertoire"""

    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title
    
    def pdf_file(self, user):
        """Returns the PDF that contains the users favorite parts for the scores in this repertoire"""
        parts = []
        for entry in self.entries.all():
            for pdf in entry.score.pdfs.all():
                parts += pdf.parts.all()
        parts = list(filter(lambda part: part.is_favorite_for(user), parts))
        if len(parts) < 1:
            raise Exception(f"Fann inga favorittstemmer for {user} i repertoaret {self}")
        pdf_writer = PdfFileWriter()
        for part in parts:
            pdf = PdfFileReader(part.pdf.file.path)
            for page_nr in range(part.from_page, part.to_page + 1):
                pdf_writer.addPage(pdf.getPage(page_nr - 1))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        return output_stream.getvalue()


class RepertoireEntry(models.Model):
    """Model representing a score entry in a repertoire"""

    repertoire = models.ForeignKey(
        Repertoire, on_delete=models.CASCADE, related_name="entries"
    )
    score = models.ForeignKey(
        sheetmusic.models.Score,
        on_delete=models.CASCADE,
        related_name="repertoireEntries",
    )

    def __str__(self):
        return f"{self.repertoire} - {self.score}"
