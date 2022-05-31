# Generated by Django 4.0.2 on 2022-02-12 11:45

import autoslug.fields
import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models

import common.forms.validators
import sheetmusic.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("instruments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Score",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="lagt ut"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="redigert"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="tittel")),
                ("content", models.TextField(blank=True, verbose_name="beskriving")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="title",
                        unique=True,
                        verbose_name="lenkjenamn",
                    ),
                ),
                (
                    "arrangement",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="arrangement"
                    ),
                ),
                (
                    "originally_from",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="opphaveleg ifrå"
                    ),
                ),
                (
                    "sound_file",
                    models.FileField(
                        blank=True,
                        default="",
                        upload_to="sheetmusic/sound_files/",
                        validators=[
                            common.forms.validators.FileTypeValidator(
                                {
                                    "audio/flac": [".flac"],
                                    "audio/midi": [".midi", ".mid"],
                                    "audio/mp4": [".mp4", ".m4a"],
                                    "audio/mpeg": [".mp3"],
                                    "audio/ogg": [".ogg"],
                                }
                            )
                        ],
                        verbose_name="lydfil",
                    ),
                ),
                ("sound_link", models.URLField(blank=True, verbose_name="lydlenkje")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="laga av",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="redigert av",
                    ),
                ),
            ],
            options={
                "verbose_name": "note",
                "verbose_name_plural": "notar",
                "ordering": ["title", "-created"],
            },
        ),
        migrations.CreateModel(
            name="Pdf",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        default=None,
                        max_length=255,
                        upload_to="sheetmusic/original_pdfs/",
                        validators=[
                            common.forms.validators.FileTypeValidator(
                                {
                                    "application/pdf": [".pdf"],
                                    "application/x-bzpdf": [".pdf"],
                                    "application/x-gzpdf": [".pdf"],
                                    "application/x-pdf": [".pdf"],
                                }
                            )
                        ],
                        verbose_name="fil",
                    ),
                ),
                (
                    "filename_original",
                    models.CharField(max_length=255, verbose_name="opphaveleg filnamn"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from=sheetmusic.models.pdf_filename_no_extension,
                        unique_with=("score__slug",),
                        verbose_name="lenkjenamn",
                    ),
                ),
                (
                    "processing",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="prosessering pågår"
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="tidsmerke"),
                ),
                (
                    "score",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pdfs",
                        to="sheetmusic.score",
                        verbose_name="note",
                    ),
                ),
            ],
            options={
                "verbose_name": "pdf",
                "verbose_name_plural": "pdfar",
                "ordering": ["filename_original"],
            },
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "part_number",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="stemmenummer"
                    ),
                ),
                (
                    "note",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="merknad"
                    ),
                ),
                (
                    "from_page",
                    models.IntegerField(
                        default=None,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="første side",
                    ),
                ),
                (
                    "to_page",
                    models.IntegerField(
                        default=None,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="siste side",
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="tidsmerke"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from=sheetmusic.models.Part.__str__,
                        unique_with=("pdf__score__slug",),
                        verbose_name="lenkjenamn",
                    ),
                ),
                (
                    "instrument_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="instruments.instrumenttype",
                        verbose_name="instrumenttype",
                    ),
                ),
                (
                    "pdf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="sheetmusic.pdf",
                        verbose_name="pdf",
                    ),
                ),
            ],
            options={
                "verbose_name": "stemme",
                "verbose_name_plural": "stemmer",
                "ordering": [
                    "instrument_type",
                    django.db.models.expressions.OrderBy(
                        django.db.models.expressions.F("part_number"), nulls_first=True
                    ),
                    "note",
                ],
            },
        ),
        migrations.CreateModel(
            name="FavoritePart",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favoring_users",
                        to="sheetmusic.part",
                        verbose_name="stemme",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_parts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="brukar",
                    ),
                ),
            ],
            options={
                "verbose_name": "favorittstemme",
                "verbose_name_plural": "favorittstemmer",
                "ordering": ["user", "part"],
            },
        ),
        migrations.AddConstraint(
            model_name="part",
            constraint=models.UniqueConstraint(
                django.db.models.expressions.F("pdf"),
                django.db.models.expressions.F("instrument_type"),
                django.db.models.expressions.F("part_number"),
                django.db.models.expressions.F("note"),
                name="unique_part",
            ),
        ),
        migrations.AddConstraint(
            model_name="favoritepart",
            constraint=models.UniqueConstraint(
                fields=("user", "part"), name="unique_user_part"
            ),
        ),
    ]
