# Generated by Django 4.1 on 2022-08-29 17:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quotes", "0003_rename_owner_quote_context_rename_text_quote_quote_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                related_name="quotes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="medlem som vert sitert",
            ),
        ),
        migrations.AlterField(
            model_name="quote",
            name="quote",
            field=models.TextField(verbose_name="sitat"),
        ),
        migrations.AlterField(
            model_name="quote",
            name="quoted_as",
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name="sitert som (med eventuell kontekst)",
            ),
        ),
    ]