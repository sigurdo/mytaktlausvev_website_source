# Generated by Django 4.0.3 on 2022-03-31 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_usercustom_light_mode"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercustom",
            name="has_storage_access",
            field=models.BooleanField(
                default=False,
                help_text="Om brukaren har fått tilgjenge til lageret.",
                verbose_name="har lagertilgjenge",
            ),
        ),
    ]
