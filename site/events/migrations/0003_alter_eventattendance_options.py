# Generated by Django 3.2.10 on 2021-12-14 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventattendance',
            options={'ordering': ['person__pk'], 'verbose_name': 'hendingdeltaking', 'verbose_name_plural': 'hendingdeltakingar'},
        ),
    ]
