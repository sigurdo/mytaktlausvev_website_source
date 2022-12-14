# Generated by Django 4.0.2 on 2022-03-01 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uniforms", "0002_alter_jacket_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jacket",
            name="state",
            field=models.CharField(
                choices=[
                    ("GOOD", "God"),
                    ("NEEDS_REPAIR", "Treng reparasjon"),
                    ("UNUSABLE", "Ikkje brukbar"),
                ],
                default="GOOD",
                max_length=255,
                verbose_name="tilstand",
            ),
        ),
    ]
