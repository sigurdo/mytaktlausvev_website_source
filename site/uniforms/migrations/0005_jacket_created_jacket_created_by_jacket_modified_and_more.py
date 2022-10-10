# Generated by Django 4.1 on 2022-10-10 13:35

import django.db.models.deletion
import django_userforeignkey.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("uniforms", "0004_auto_20220301_1534"),
    ]

    operations = [
        migrations.AddField(
            model_name="jacket",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="lagt ut",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="jacket",
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
            model_name="jacket",
            name="modified",
            field=models.DateTimeField(auto_now=True, verbose_name="redigert"),
        ),
        migrations.AddField(
            model_name="jacket",
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
        migrations.AddField(
            model_name="jacket",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="jacket",
                to=settings.AUTH_USER_MODEL,
                verbose_name="eigar",
            ),
        ),
        migrations.AddField(
            model_name="jacket",
            name="state_comment",
            field=models.TextField(blank=True, verbose_name="tilstandskommentar"),
        ),
    ]
