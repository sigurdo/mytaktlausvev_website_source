# Generated by Django 4.1 on 2022-08-24 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_eventkeyinfoentry_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventCategory",
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
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="Namn"),
                ),
            ],
            options={
                "verbose_name": "hendingskategori",
                "verbose_name_plural": "hendingskategoriar",
            },
        ),
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events",
                to="events.eventcategory",
                verbose_name="Kategori",
            ),
        ),
    ]
