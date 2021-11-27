""" Models for the sheetmusic-app """

import os
import shutil
import multiprocessing

import django
from django.db import models
from django.conf import settings
from django.utils import timezone

from upload_validator import FileTypeValidator
from sheatless import processUploadedPdf

from web.settings import BASE_DIR


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
                    "tessdata_dir": os.path.join(
                        BASE_DIR, "..", "tessdata", "tessdata_best-4.1.0"
                    ),
                },
            )
            for part in parts:
                part = Part(
                    name=part["name"],
                    pdf=self,
                    from_page=part["fromPage"],
                    to_page=part["toPage"],
                    timestamp=timezone.now(),
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
    from_page = models.IntegerField("første side", default=None)
    to_page = models.IntegerField("siste side", default=None)
    timestamp = models.DateTimeField("tidsmerke", auto_now_add=True)

    class Meta:
        ordering = ["pdf", "from_page", "to_page", "name"]
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"

    def __str__(self):
        return self.name


class UsersPreferredPart(models.Model):
    """Model representing the preferred part of a user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="brukar", on_delete=models.CASCADE
    )
    part = models.ForeignKey(Part, verbose_name="stemme", on_delete=models.CASCADE)

    class Meta:
        ordering = ["user", "part"]
        verbose_name = "brukarfavorittstemme"
        verbose_name_plural = "brukarfavorittstemmer"

    def __str__(self):
        return f"{self.user}-{self.part}"
