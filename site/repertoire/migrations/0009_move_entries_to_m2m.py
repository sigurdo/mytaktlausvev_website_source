# Generated by Django 4.1 on 2022-10-13 15:34

from django.db import migrations


def move_entries_to_many_to_many_field(apps, schema_editor):
    Repertoire = apps.get_model("repertoire", "Repertoire")
    for repertoire in Repertoire.objects.all():
        for entry in repertoire.entries.all():
            repertoire.scores.add(entry.score)


class Migration(migrations.Migration):

    dependencies = [
        ("repertoire", "0008_repertoire_scores"),
    ]

    operations = [migrations.RunPython(move_entries_to_many_to_many_field)]