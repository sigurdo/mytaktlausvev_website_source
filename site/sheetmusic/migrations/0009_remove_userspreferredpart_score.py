# Generated by Django 3.2.7 on 2021-10-01 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0008_auto_20210513_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userspreferredpart',
            name='score',
        ),
    ]
