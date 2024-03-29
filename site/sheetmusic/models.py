""" Models for the sheetmusic-app """

import io
import os
from zipfile import ZIP_DEFLATED, ZipFile

from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    Exists,
    F,
    FileField,
    ForeignKey,
    IntegerField,
    Manager,
    Model,
    OuterRef,
    TextField,
    UniqueConstraint,
    URLField,
)
from django.urls import reverse
from django.utils.text import get_valid_filename
from pypdf import PdfMerger, PdfReader, PdfWriter
from sheatless import PdfPredictor, predict_part_from_string

from common.forms.validators import FileTypeValidator
from common.models import ArticleMixin
from instruments.models import InstrumentType
from web.settings import TESSDATA_DIR


class ScoreManager(Manager):
    def annotate_user_has_favorite_parts(self, user):
        return super().annotate(
            user_has_favorite_parts=Exists(
                FavoritePart.objects.filter(part__pdf__score=OuterRef("pk"), user=user)
            )
        )


class Score(ArticleMixin):
    """Model representing a score"""

    objects = ScoreManager()
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
    transcribed_by = CharField(
        verbose_name="transkribert av", blank=True, max_length=255
    )
    sound_file = FileField(
        verbose_name="lydfil",
        upload_to="sheetmusic/sound_files/",
        blank=True,
        default="",
        validators=[
            FileTypeValidator(
                [".mp3", ".midi", ".mid", ".ogg", ".mp4", ".m4a", ".flac"]
            )
        ],
    )
    sound_link = URLField(verbose_name="lydlenkje", blank=True)

    class Meta:
        ordering = ["title", "-created"]
        verbose_name = "note"
        verbose_name_plural = "notar"

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.slug})

    def find_user_part(self, user):
        """
        Finds the most relevant part for user by the following priority:
        1. One of user's favorite parts
        2. A part for user's instrument type
        3. A part for another instrument type in user's instrument group
        4. None
        """
        all_parts = Part.objects.filter(pdf__score=self)
        favorite_parts = all_parts.filter(favoring_users__user=user)
        if favorite_parts.exists():
            return favorite_parts.first()
        if user.instrument_type:
            instrument_parts = all_parts.filter(instrument_type=user.instrument_type)
            if instrument_parts.exists():
                return instrument_parts.first()
            group_parts = all_parts.filter(
                instrument_type__group=user.instrument_type.group
            )
            if group_parts.exists():
                return group_parts.first()
        return None

    def favorite_parts_pdf_file(self, user):
        """Returns the PDF that contains user's favorite parts on this score"""
        parts = Part.objects.filter(favoring_users__user=user, pdf__score=self)
        if not parts.exists():
            raise Exception(f"Fann inga favorittstemmer for {user} for nota {self}")
        pdf_writer = PdfWriter()
        for part in parts:
            pdf_writer.append_pages_from_reader(PdfReader(part.pdf_file()))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def favorite_parts_pdf_filename(self, user):
        return get_valid_filename(f"{self.title} {user}.pdf")

    def pdf_filename(self):
        """Returns a nice filename for a PDF containing all parts of this score."""
        return get_valid_filename(f"{self.title} Alle stemmer.pdf")

    def pdf_file(self):
        """Returns a PDF containing all parts of this score."""
        pdf_merger = PdfMerger()
        for part in Part.objects.filter(pdf__score=self):
            part_pdf_stream = part.pdf_file()
            part_pdf_reader = PdfReader(part_pdf_stream)
            pdf_merger.append(part_pdf_reader)
        pdf_stream = io.BytesIO()
        pdf_merger.write(pdf_stream)
        pdf_stream.seek(0)
        pdf_name = self.pdf_filename()
        return pdf_stream, pdf_name

    def zip_filename(self):
        """Returns a nice filename for a ZIP file containing all parts of this score."""
        return get_valid_filename(f"{self.title} Alle stemmer.zip")

    def zip_file(self):
        """Returns a ZIP file containing all parts of this score."""
        zip_stream = io.BytesIO()
        with ZipFile(zip_stream, mode="w", compression=ZIP_DEFLATED) as zip:
            for part in Part.objects.filter(pdf__score=self):
                pdf_stream = part.pdf_file()
                pdf_filename = part.pdf_filename()
                zip.writestr(pdf_filename, pdf_stream.read())
        zip_stream.seek(0)
        zip_name = self.zip_filename()
        return zip_stream, zip_name

    def is_processing(self):
        return self.pdfs.filter(processing=True).exists()


pdf_file_validators = [FileTypeValidator([".pdf"])]


def pdf_filename_no_extension(pdf):
    return pdf.filename_no_extension()


class Pdf(Model):
    """Model representing an uploaded pdf"""

    score = ForeignKey(
        Score, verbose_name="note", on_delete=CASCADE, related_name="pdfs"
    )
    file = FileField(
        "fil",
        upload_to="sheetmusic/original_pdfs/",
        default=None,
        validators=pdf_file_validators,
        # We need a larger max file path length
        # because some of our PDFs have really long names
        max_length=255,
    )
    filename_original = CharField("opphaveleg filnamn", max_length=255)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from=pdf_filename_no_extension,
        unique_with="score__slug",
        editable=True,
    )
    processing = BooleanField("prosessering pågår", default=False, editable=False)
    timestamp = DateTimeField("tidsmerke", auto_now_add=True)

    class Meta:
        ordering = ["filename_original"]
        verbose_name = "pdf"
        verbose_name_plural = "pdfar"

    def __str__(self):
        return self.filename_original

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.score.slug})

    def filename_no_extension(self):
        """Returns the original filename of the PDF, without a file extension."""
        return os.path.splitext(self.filename_original)[0]

    def num_of_pages(self):
        pdf_reader = PdfReader(self.file.open(), strict=False)
        return len(pdf_reader.pages)

    def find_parts_with_sheatless(self):
        self.processing = True
        self.save()
        try:
            with self.file.open() as pdf_file:
                pdf_predictor = PdfPredictor(
                    pdf_file.read(),
                    use_lstm=True,
                    crop_to_left=True,
                    crop_to_top=True,
                    tessdata_dir=TESSDATA_DIR,
                    tesseract_languages=["nor"],
                    instruments=InstrumentType.objects.sheatless_format(),
                    full_score_threshold=2,
                    full_score_label="Partitur",
                )

            for part in pdf_predictor.parts():
                for instrument_name in part["instruments"]:
                    instrument_type = InstrumentType.objects.filter(
                        name__iexact=instrument_name
                    ).first()
                    if not instrument_type:
                        instrument_type = InstrumentType.unknown()
                    self.create_part_auto_number(
                        instrument_type=instrument_type,
                        note="funne automatisk",
                        from_page=part["fromPage"],
                        to_page=part["toPage"],
                    )
        finally:
            self.processing = False
            self.save()

    def find_parts_from_original_filename(self):
        filename, _ = os.path.splitext(self.filename_original)
        part = predict_part_from_string(
            filename,
            instruments=InstrumentType.objects.sheatless_format(),
        )
        if part is None:
            return
        part_number, instruments = part
        for instrument_name in instruments:
            instrument_type = InstrumentType.objects.filter(
                name__iexact=instrument_name
            ).first()
            if not instrument_type:
                instrument_type = InstrumentType.unknown()
            self.create_part_auto_number(
                instrument_type=instrument_type,
                note="funne automatisk",
                from_page=1,
                to_page=self.num_of_pages(),
            )

    def create_part_auto_number(self, **kwargs):
        """
        Creates a new Part with part_number caclulated automatically.
        """
        part_number = None
        other_parts_for_same_instrument = Part.objects.filter(
            pdf__score=self.score, instrument_type=kwargs["instrument_type"]
        ).order_by(F("part_number").asc(nulls_first=True))
        if other_parts_for_same_instrument.exists():
            if other_parts_for_same_instrument.count() == 1:
                part_one = other_parts_for_same_instrument.first()
                part_one.part_number = 1
                part_one.save()
            part_number = (other_parts_for_same_instrument.last().part_number or 0) + 1
        Part(
            part_number=part_number,
            pdf=self,
            **kwargs,
        ).save()


class PartManager(Manager):
    def get_queryset(self):
        """
        Since `instrument_type` is used in Part's string function,
        always querying for it ahead of time often leads to a performance boost.
        """
        return super().get_queryset().select_related("instrument_type")

    def annotate_is_favorite(self, user):
        return super().annotate(
            is_favorite=Exists(user.favorite_parts.filter(part=OuterRef("pk")))
        )


class Part(Model):
    """Model representing a part"""

    objects = PartManager()

    instrument_type = ForeignKey(
        InstrumentType,
        verbose_name="instrumenttype",
        related_name="parts",
        on_delete=CASCADE,
    )
    part_number = IntegerField(verbose_name="stemmenummer", blank=True, null=True)
    note = CharField(verbose_name="merknad", max_length=255, blank=True)
    pdf = ForeignKey(Pdf, verbose_name="pdf", on_delete=CASCADE, related_name="parts")
    from_page = IntegerField(
        "første side", default=None, validators=[MinValueValidator(1)]
    )
    to_page = IntegerField(
        "siste side", default=None, validators=[MinValueValidator(1)]
    )
    timestamp = DateTimeField("tidsmerke", auto_now_add=True)

    def __str__(self):
        result = str(self.instrument_type)
        if self.part_number:
            result += f" {self.part_number}"
        if self.note:
            result += f" ({self.note})"
        return result

    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from=__str__,
        unique_with="pdf__score__slug",
        editable=True,
        always_update=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["pdf", "instrument_type", "part_number", "note"],
                name="unique_part",
            )
        ]
        ordering = ["instrument_type", F("part_number").asc(nulls_first=True), "note"]
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"

    def get_absolute_url(self):
        return reverse(
            "sheetmusic:PartDetail",
            kwargs={"score_slug": self.pdf.score.slug, "slug": self.slug},
        )

    def get_pdf_url(self):
        return reverse(
            "sheetmusic:PartPdf",
            kwargs={"score_slug": self.pdf.score.slug, "slug": self.slug},
        )

    def pdf_file(self):
        """Returns the PDF that contains only this part"""
        pdf = PdfReader(self.pdf.file.open())
        pdf_writer = PdfWriter()
        for page_nr in range(self.from_page, self.to_page + 1):
            pdf_writer.add_page(pdf.pages[page_nr - 1])
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return output_stream

    def pdf_filename(self):
        """Returns a nice filename for the PDF that contains only this part"""
        return get_valid_filename(f"{self.pdf.score.title} {self}.pdf")


class FavoritePart(Model):
    """Model representing a favorite part of a user"""

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="brukar",
        on_delete=CASCADE,
        related_name="favorite_parts",
    )
    part = ForeignKey(
        Part,
        verbose_name="stemme",
        on_delete=CASCADE,
        related_name="favoring_users",
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "part"], name="unique_user_part")
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


class EditFile(Model):
    """Model representing an edit file for a score."""

    score = ForeignKey(
        Score, verbose_name="note", on_delete=CASCADE, related_name="edit_files"
    )
    file = FileField(
        "fil",
        upload_to="sheetmusic/edit_files/",
        validators=[FileTypeValidator([".mscz", ".mscx", ".niff", ".sib", ".musx"])],
        max_length=255,
    )
    filename_original = CharField("opphaveleg filnamn", max_length=255)
    timestamp = DateTimeField("tidsmerke", auto_now_add=True)

    def __str__(self):
        return self.filename_original

    def get_absolute_url(self):
        return reverse("sheetmusic:ScoreView", kwargs={"slug": self.score.slug})

    class Meta:
        ordering = ["filename_original"]
        verbose_name = "redigeringsfil"
        verbose_name_plural = "redigeringsfiler"
