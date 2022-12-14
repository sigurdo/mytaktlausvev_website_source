# Generated by Django 4.1 on 2022-10-19 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pictures", "0003_alter_gallery_created_by_alter_gallery_modified_by"),
        ("events", "0010_event_extra_scores_event_include_active_repertoires_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="gallery",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="events",
                to="pictures.gallery",
                verbose_name="galleri",
            ),
        ),
    ]
