# Generated by Django 4.1 on 2022-08-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "instruments",
            "0002_alter_instrument_options_remove_instrument_group_and_more",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="instrument",
            name="unique_instrument",
        ),
        migrations.AddConstraint(
            model_name="instrument",
            constraint=models.UniqueConstraint(
                fields=("type", "identifier"), name="unique_instrument"
            ),
        ),
    ]
