# Generated by Django 4.1 on 2022-10-07 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("instruments", "0003_remove_instrument_unique_instrument_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="instrument",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="lagt ut",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="instrument",
            name="created_by",
            field=django_userforeignkey.models.fields.UserForeignKey(
                blank=True,
                null=True,
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="laga av",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="instrument",
            name="modified",
            field=models.DateTimeField(auto_now=True, verbose_name="redigert"),
        ),
        migrations.AddField(
            model_name="instrument",
            name="modified_by",
            field=django_userforeignkey.models.fields.UserForeignKey(
                blank=True,
                null=True,
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
                verbose_name="redigert av",
            ),
            preserve_default=False,
        ),
    ]
