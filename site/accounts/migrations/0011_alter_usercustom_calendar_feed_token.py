# Generated by Django 4.0.3 on 2022-05-26 13:18

from django.db import migrations, models
import secrets


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_data_migration_usercustom_calendar_feed_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercustom',
            name='calendar_feed_token',
            field=models.CharField(default=secrets.token_urlsafe, max_length=255, unique=True, verbose_name='Kalenderfeedtoken'),
        ),
    ]
