# Generated by Django 4.1 on 2022-08-29 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Orchestra",
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
                ("name", models.CharField(max_length=255, verbose_name="Namn")),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("TRONDHEIM", "Trondheim"),
                            ("ÅS", "Ås"),
                            ("OSLO", "Oslo"),
                            ("KRISTIANSAND", "Kristiansand"),
                            ("BERGEN", "Bergen"),
                            ("TROMSØ", "Tromsø"),
                        ],
                        max_length=255,
                        verbose_name="By",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, upload_to="orchestras/", verbose_name="logo"
                    ),
                ),
            ],
        ),
    ]
