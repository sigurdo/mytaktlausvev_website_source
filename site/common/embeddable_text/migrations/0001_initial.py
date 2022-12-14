# Generated by Django 4.0.3 on 2022-05-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmbeddableText",
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
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="namn"),
                ),
                (
                    "content",
                    models.TextField(blank=True, default="", verbose_name="innhald"),
                ),
            ],
            options={
                "verbose_name": "innbyggbar tekst",
                "verbose_name_plural": "innbyggbare tekster",
                "ordering": ["name"],
            },
        ),
    ]
