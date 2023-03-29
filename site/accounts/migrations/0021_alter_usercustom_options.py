# Generated by Django 4.1 on 2023-01-22 21:50

import django.db.models.functions.comparison
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0020_alter_usercustom_image_sharing_consent"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="usercustom",
            options={
                "ordering": [
                    django.db.models.functions.text.Lower(
                        django.db.models.functions.comparison.NullIf(
                            "name", models.Value("")
                        ),
                        nulls_last=True,
                    )
                ],
                "permissions": (
                    ("view_storage_access", "Kan sjå lagertilgjenge"),
                    ("edit_storage_access", "Kan redigere lagertilgjenge"),
                    (
                        "view_image_sharing_consent",
                        "Kan sjå samtykkje til deling av bilete",
                    ),
                    (
                        "view_calendar_feed_settings",
                        "Kan sjå innstillinger for kalenderintegrasjon",
                    ),
                    (
                        "edit_instrument_group_leaders",
                        "Kan redigere instrumentgruppeleiarar",
                    ),
                ),
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
    ]