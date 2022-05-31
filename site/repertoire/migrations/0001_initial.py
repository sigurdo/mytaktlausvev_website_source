# Generated by Django 4.0.2 on 2022-02-12 11:45

import autoslug.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sheetmusic", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Repertoire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="namn")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now_add=True, verbose_name="tidsmerke"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="name",
                        unique=True,
                        verbose_name="lenkjenamn",
                    ),
                ),
                (
                    "order",
                    models.FloatField(
                        default=0,
                        help_text="Definerer rekkjefølgja til repertoaret. Repertoar med lik rekkjefølgje vert sortert etter namn.",
                        verbose_name="rekkjefølgje",
                    ),
                ),
            ],
            options={
                "verbose_name": "repertoar",
                "verbose_name_plural": "repertoar",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="RepertoireEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "repertoire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="repertoire.repertoire",
                        verbose_name="repertoar",
                    ),
                ),
                (
                    "score",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repertoire_entries",
                        to="sheetmusic.score",
                        verbose_name="note",
                    ),
                ),
            ],
            options={
                "verbose_name": "repertoaroppføring",
                "verbose_name_plural": "repertoaroppføringar",
            },
        ),
        migrations.AddConstraint(
            model_name="repertoire",
            constraint=models.UniqueConstraint(
                fields=("slug",), name="repertoire_unique_slug"
            ),
        ),
        migrations.AddConstraint(
            model_name="repertoireentry",
            constraint=models.UniqueConstraint(
                fields=("repertoire", "score"), name="repertoire_unique_entry"
            ),
        ),
    ]
