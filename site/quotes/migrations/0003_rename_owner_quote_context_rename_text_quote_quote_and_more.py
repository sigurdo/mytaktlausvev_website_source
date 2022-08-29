# Generated by Django 4.1 on 2022-08-19 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quotes", "0002_alter_quote_created_by_alter_quote_modified_by"),
    ]

    operations = [
        migrations.RenameField(
            model_name="quote",
            old_name="owner",
            new_name="quoted_as",
        ),
        migrations.RenameField(
            model_name="quote",
            old_name="text",
            new_name="quote",
        ),
        migrations.RemoveField(
            model_name="quote",
            name="timestamp",
        ),
    ]
