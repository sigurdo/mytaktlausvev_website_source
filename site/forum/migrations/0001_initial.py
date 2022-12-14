# Generated by Django 4.0.2 on 2022-02-12 11:45

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Forum",
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
                ("title", models.CharField(max_length=255, verbose_name="tittel")),
                (
                    "description",
                    models.CharField(max_length=255, verbose_name="beskriving"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="title",
                        unique=True,
                        verbose_name="lenkjenamn",
                    ),
                ),
            ],
            options={
                "verbose_name": "forum",
                "verbose_name_plural": "forum",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Topic",
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
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="lagt ut"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="redigert"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="tittel")),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="title",
                        unique_with=("forum",),
                        verbose_name="lenkjenamn",
                    ),
                ),
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
                    "forum",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="topics",
                        to="forum.forum",
                        verbose_name="forum",
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
                "verbose_name": "emne",
                "verbose_name_plural": "emne",
            },
        ),
    ]
