""" Models for the sheetmusic-app """

import os
import shutil
import multiprocessing
import io

import django
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CharField, DateTimeField, TextField, URLField, FileField
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


from upload_validator import FileTypeValidator
from sheatless import processUploadedPdf
from PyPDF2 import PdfFileReader, PdfFileWriter
from autoslug import AutoSlugField

from web.settings import TESSDATA_DIR


class Score(models.Model):
    """Model representing a score"""

    title = CharField("tittel", max_length=255)
    timestamp = DateTimeField("tidsmerke", auto_now_add=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique=True,
        editable=True,
    )
    arrangement = CharField(verbose_name="arrangement", blank=True, max_length=255)
    originally_from = CharField(
        verbose_name="originalt ifrå", blank=True, max_length=255
    )
    description = TextField(verbose_name="beskriving", blank=True)
    sound_file = FileField(
        verbose_name="lydfil",
        upload_to="sheetmusic/sound_files/",
        blank=True,
        null=True,
        default=None,
    )
    sound_link = URLField(verbose_name="lydlenkje", blank=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "note"
        verbose_name_plural = "notar"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.slug})


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
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.score.slug})

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

            # PDF processing is done in a separate process to not affect response time
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


@receiver(pre_delete, sender=Pdf, dispatch_uid="pdf_delete_images")
def pdf_pre_delete_receiver(sender, instance: Pdf, using, **kwargs):
    """
    Delete pdf file and all related images from filesystem
    """
    # Delete related images
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
    # Delete pdf file
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
        return output_stream.getvalue()

    def pdf_basefilename_slug(self):
        """Returns a nice filename slug for the PDF that contains only this part"""
        return slugify(f"{self.pdf.score.title} {self.name}")

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
