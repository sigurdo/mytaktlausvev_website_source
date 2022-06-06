# Generated by Django 4.0.3 on 2022-05-26 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_usercustom_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercustom",
            name="calendar_feed_start_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Startdato for kalenderfeed"
            ),
        ),
        migrations.AddField(
            model_name="usercustom",
            name="calendar_feed_token",
            field=models.CharField(
                default="", max_length=255, verbose_name="Kalenderfeedtoken"
            ),
        ),
    ]