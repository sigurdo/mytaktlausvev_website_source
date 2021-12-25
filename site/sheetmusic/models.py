""" Models for the sheetmusic-app """

import io
import multiprocessing
import os

from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField, FileField, TextField, URLField
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from PyPDF2 import PdfFileReader, PdfFileWriter
from sheatless import predict_parts_in_pdf

from common.models import ArticleMixin
from common.validators import FileTypeValidator
from web.settings import TESSDATA_DIR


class Score(ArticleMixin):
    """Model representing a score"""

    # Override content to get a more suitable verbose_name
    content = TextField(verbose_name="beskriving", blank=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique=True,
        editable=True,
    )
    arrangement = CharField(verbose_name="arrangement", blank=True, max_length=255)
    originally_from = CharField(
        verbose_name="opphaveleg ifrå", blank=True, max_length=255
    )
    sound_file = FileField(
        verbose_name="lydfil",
        upload_to="sheetmusic/sound_files/",
        blank=True,
        default="",
        validators=[
            FileTypeValidator(
                {
                    "audio/mpeg": [".mp3"],
                    "audio/midi": [".midi", ".mid"],
                    "audio/ogg": [".ogg"],
                    "audio/mp4": [".mp4", ".m4a"],
                    "audio/flac": [".flac"],
                },
            )
        ],
    )
    sound_link = URLField(verbose_name="lydlenkje", blank=True)

    class Meta:
        ordering = ["title", "-submitted"]
        verbose_name = "note"
        verbose_name_plural = "notar"

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.slug})

    def favorite_parts_pdf_file(self, user):
        """Returns the PDF that contains user's favorite parts on this score"""
        parts = Part.objects.filter(favoring_users__user=user, pdf__score=self)
        if not parts.exists():
            raise Exception(f"Fann inga favorittstemmer for {user} for nota {self}")
        pdf_writer = PdfFileWriter()
        for part in parts:
            pdf_writer.appendPagesFromReader(PdfFileReader(part.pdf_file()))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def favorite_parts_pdf_filename(self, user):
        return slugify(f"{self.title} {user}") + ".pdf"


@receiver(pre_save, sender=Score, dispatch_uid="score_pre_save_receiver")
def score_pre_save_receiver(sender, instance: Score, using, **kwargs):
    """
    Delete eventual old sound_file from filesystem
    """
    if not instance.pk:
        return

    try:
        old_file = Score.objects.get(pk=instance.pk).sound_file
    except Score.DoesNotExist:
        return

    new_file = instance.sound_file
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


pdf_file_validators = [
    FileTypeValidator(
        {
            "application/pdf": [".pdf"],
            "application/x-pdf": [".pdf"],
            "application/x-bzpdf": [".pdf"],
            "application/x-gzpdf": [".pdf"],
        }
    ),
]


def pdf_get_base_filename(pdf):
    return pdf.get_base_filename()


class Pdf(models.Model):
    """Model representing an uploaded pdf"""

    score = models.ForeignKey(
        Score, verbose_name="note", on_delete=models.CASCADE, related_name="pdfs"
    )
    file = models.FileField(
        "fil",
        upload_to="sheetmusic/original_pdfs/",
        default=None,
        validators=pdf_file_validators,
    )
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from=pdf_get_base_filename,
        unique_with="score__slug",
        editable=True,
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
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.score.slug})

    def get_base_filename(self):
        """Returns the base filename of the pdf file without file extension."""
        filepath = str(self.file)
        filename = os.path.basename(filepath)
        filename_no_ext = os.path.splitext(filename)[0]
        return filename_no_ext

    def num_of_pages(self):
        pdf_reader = PdfFileReader(self.file.path)
        return pdf_reader.getNumPages()

    def find_parts(self):
        self.processing = True
        self.save()
        try:
            # PDF processing is done in a separate process to not affect response time
            # of other requests the server receives while it is processing
            with open(self.file.path, "rb") as pdf_file:
                parts, instrumentsDefaultParts = multiprocessing.Pool().apply(
                    predict_parts_in_pdf,
                    [pdf_file.read()],
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


@receiver(pre_delete, sender=Pdf, dispatch_uid="pdf_delete_images")
def pdf_pre_delete_receiver(sender, instance: Pdf, using, **kwargs):
    """
    Delete pdf file from filesystem
    """
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
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="name",
        unique_with="pdf__score__slug",
        editable=True,
    )

    class Meta:
        ordering = ["pdf", "from_page", "to_page", "name"]
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.pdf.score.slug})

    def pdf_file(self):
        """Returns the PDF that contains only this part"""
        pdf = PdfFileReader(self.pdf.file.path)
        pdf_writer = PdfFileWriter()
        for page_nr in range(self.from_page, self.to_page + 1):
            pdf_writer.addPage(pdf.getPage(page_nr - 1))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def pdf_filename(self):
        """Returns a nice filename for the PDF that contains only this part"""
        return slugify(f"{self.pdf.score.title} {self.name}") + ".pdf"

    def is_favorite_for(self, user):
        return user.favorite_parts.filter(part=self).exists()


class FavoritePart(models.Model):
    """Model representing a favorite part of a user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=models.CASCADE,
        related_name="favorite_parts",
    )
    part = models.ForeignKey(
        Part,
        verbose_name="stemme",
        on_delete=models.CASCADE,
        related_name="favoring_users",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "part"], name="unique_user_part")
        ]
        ordering = ["user", "part"]
        verbose_name = "favorittstemme"
        verbose_name_plural = "favorittstemmer"

    def __str__(self):
        return f"{self.user}-{self.part}"

    def get_absolute_url(self):
        return reverse(
            "sheetmusic:ScoreView", kwargs={"slug": self.part.pdf.score.slug}
        )
