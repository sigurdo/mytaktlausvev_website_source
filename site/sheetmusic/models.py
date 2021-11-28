""" Models for the sheetmusic-app """

import os
import shutil
import multiprocessing
import io

import django
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


from upload_validator import FileTypeValidator
from sheatless import processUploadedPdf
from PyPDF2 import PdfFileReader, PdfFileWriter

from web.settings import TESSDATA_DIR


class Score(models.Model):
    """Model representing a score"""

    title = models.CharField("tittel", max_length=255)
    timestamp = models.DateTimeField("tidsmerke", auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "note"
        verbose_name_plural = "notar"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"pk": self.pk})


class Pdf(models.Model):
    """Model representing an uploaded pdf"""

    score = models.ForeignKey(
        Score, verbose_name="note", on_delete=models.CASCADE, related_name="pdfs"
    )
    file = models.FileField(
        "fil",
        upload_to="sheetmusic/original_pdfs/",
        default=None,
        validators=[
            FileTypeValidator(
                allowed_types=[
                    "application/pdf",
                    "application/x-pdf",
                    "application/x-bzpdf",
                    "application/x-gzpdf",
                ],
                allowed_extensions=[".pdf", ".PDF"],
            )
        ],
    )
    processing = models.BooleanField(
        "prosessering pågår", default=False, editable=False
    )
    timestamp = models.DateTimeField("tidsmerke", auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "pdf"
        verbose_name_plural = "pdfar"

    def __str__(self):
        return os.path.basename(self.file.path)

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"pk": self.score.pk})

    def find_parts(self):
        self.processing = True
        self.save()
        try:
            imagesDirPath = os.path.join(
                django.conf.settings.MEDIA_ROOT, "sheetmusic", "images"
            )
            if not os.path.exists(imagesDirPath):
                os.mkdir(imagesDirPath)
            imagesDirPath = os.path.join(imagesDirPath, str(self.pk))
            if not os.path.exists(imagesDirPath):
                os.mkdir(imagesDirPath)

            # PDF processing is done in a separate process to not affect responsetime
            # of other requests the server receives while it is processing
            parts, instrumentsDefaultParts = multiprocessing.Pool().apply(
                processUploadedPdf,
                (self.file.path, imagesDirPath),
                {
                    "use_lstm": True,
                    "tessdata_dir": TESSDATA_DIR,
                },
            )
            for part in parts:
                part = Part(
                    name=part["name"],
                    pdf=self,
                    from_page=part["fromPage"],
                    to_page=part["toPage"],
                )
                part.save()
        finally:
            self.processing = False
            self.save()


@django.dispatch.receiver(
    django.db.models.signals.pre_delete, sender=Pdf, dispatch_uid="pdf_delete_images"
)
def pdf_pre_delete_receiver(sender, instance: Pdf, using, **kwargs):
    # Deleting all images related to that pdf
    if os.path.exists(
        os.path.join(
            django.conf.settings.MEDIA_ROOT, "sheetmusic", "images", str(instance.pk)
        )
    ):
        shutil.rmtree(
            os.path.join(
                django.conf.settings.MEDIA_ROOT,
                "sheetmusic",
                "images",
                str(instance.pk),
            )
        )
    # Deleting actual pdf file
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


class Part(models.Model):
    """Model representing a part"""

    name = models.CharField("namn", max_length=255)
    pdf = models.ForeignKey(
        Pdf, verbose_name="pdf", on_delete=models.CASCADE, related_name="parts"
    )
    from_page = models.IntegerField(
        "første side", default=None, validators=[MinValueValidator(1)]
    )
    to_page = models.IntegerField(
        "siste side", default=None, validators=[MinValueValidator(1)]
    )
    timestamp = models.DateTimeField("tidsmerke", auto_now_add=True)

    class Meta:
        ordering = ["pdf", "from_page", "to_page", "name"]
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"pk": self.pdf.score.pk})

    def pdf_file(self):
        """Returns the PDF that contains only this part"""
        pdf = PdfFileReader(self.pdf.file.path)
        pdf_writer = PdfFileWriter()
        for page_nr in range(self.from_page, self.to_page + 1):
            pdf_writer.addPage(pdf.getPage(page_nr - 1))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        return output_stream.getvalue()

    def pdf_filename_slug(self):
        """Returns a nice filename slug for the PDF that contains only this part"""
        return slugify(f"{self.pdf.score.title}-{self.name}") + ".pdf"

    def is_favorite_for(self, user):
        count = user.preferred_parts.filter(part=self).count()
        return True if count > 0 else False


class UsersPreferredPart(models.Model):
    """Model representing the preferred part of a user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=models.CASCADE,
        related_name="preferred_parts",
    )
    part = models.ForeignKey(
        Part,
        verbose_name="stemme",
        on_delete=models.CASCADE,
        related_name="preferring_users",
    )

    class Meta:
        ordering = ["user", "part"]
        verbose_name = "brukarfavorittstemme"
        verbose_name_plural = "brukarfavorittstemmer"

    def __str__(self):
        return f"{self.user}-{self.part}"

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"pk": self.part.pdf.score.pk})
