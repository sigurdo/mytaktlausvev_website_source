# Generated by Django 4.1 on 2023-01-16 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0019_alter_usercustom_can_wear_hats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercustom",
            name="image_sharing_consent",
            field=models.CharField(
                choices=[
                    ("YES", "Ja"),
                    ("GROUP_ONLY", "Berre gruppebilete"),
                    ("NO", "Nei"),
                    ("UNKNOWN", "Ukjent"),
                ],
                default="UNKNOWN",
                help_text="Om bilete du er med i kan delast på våre sosiale medier.",
                max_length=30,
                verbose_name="samtykkje til deling av bilete",
            ),
        ),
    ]
