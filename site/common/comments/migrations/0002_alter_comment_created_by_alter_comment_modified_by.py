# Generated by Django 4.1 on 2022-08-26 08:37

import django.db.models.deletion
import django_userforeignkey.models.fields
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
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
            model_name="comment",
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
