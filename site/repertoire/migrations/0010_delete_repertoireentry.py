# Generated by Django 4.1 on 2022-10-13 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("repertoire", "0009_move_entries_to_m2m"),
    ]

    operations = [
        migrations.DeleteModel(
            name="RepertoireEntry",
        ),
    ]
