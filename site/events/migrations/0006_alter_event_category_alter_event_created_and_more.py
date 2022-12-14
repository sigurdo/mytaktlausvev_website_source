# Generated by Django 4.1 on 2022-08-25 23:19

import django.db.models.deletion
import django_userforeignkey.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0005_eventcategory_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="events",
                to="events.eventcategory",
                verbose_name="Kategori",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="lagt ut"),
        ),
        migrations.AlterField(
            model_name="event",
            name="modified",
            field=models.DateTimeField(auto_now=True, verbose_name="redigert"),
        ),
        migrations.AlterField(
            model_name="event",
            name="created_by",
            field=django_userforeignkey.models.fields.UserForeignKey(
                blank=True,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="laga av",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="modified_by",
            field=django_userforeignkey.models.fields.UserForeignKey(
                blank=True,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
                verbose_name="redigert av",
            ),
        ),
    ]
