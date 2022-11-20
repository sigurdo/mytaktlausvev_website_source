# Generated by Django 4.1 on 2022-11-20 13:04

import django.db.models.deletion
from django.db import migrations, models

import common.forms.validators


class Migration(migrations.Migration):

    dependencies = [
        ("sheetmusic", "0006_score_transcribed_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pdf",
            name="file",
            field=models.FileField(
                default=None,
                max_length=255,
                upload_to="sheetmusic/original_pdfs/",
                validators=[common.forms.validators.FileTypeValidator([".pdf"])],
                verbose_name="fil",
            ),
        ),
        migrations.AlterField(
            model_name="score",
            name="sound_file",
            field=models.FileField(
                blank=True,
                default="",
                upload_to="sheetmusic/sound_files/",
                validators=[
                    common.forms.validators.FileTypeValidator(
                        [".mp3", ".midi", ".mid", ".ogg", ".mp4", ".m4a", ".flac"]
                    )
                ],
                verbose_name="lydfil",
            ),
        ),
        migrations.CreateModel(
            name="Original",
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
                        max_length=255,
                        upload_to="sheetmusic/originals/",
                        validators=[
                            common.forms.validators.FileTypeValidator(
                                [".mscz", ".mscx", ".niff", ".sib", ".musx"]
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
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="tidsmerke"),
                ),
                (
                    "score",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="originals",
                        to="sheetmusic.score",
                        verbose_name="note",
                    ),
                ),
            ],
            options={
                "verbose_name": "original",
                "verbose_name_plural": "originalar",
                "ordering": ["filename_original"],
            },
        ),
    ]
