# Generated by Django 4.1 on 2023-04-14 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0022_usercustom_is_active_override"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercustom",
            name="preferred_name",
            field=models.CharField(
                blank=True,
                help_text="Namnet du føretrekkjer at andre brukar.",
                max_length=255,
                verbose_name="føretrekt namn",
            ),
        ),
    ]