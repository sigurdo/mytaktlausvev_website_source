# Generated by Django 4.0 on 2021-12-24 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_alter_topic_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'get_latest_by': ['posts__submitted', 'submitted'], 'ordering': ['-posts__submitted'], 'verbose_name': 'emne', 'verbose_name_plural': 'emne'},
        ),
    ]
