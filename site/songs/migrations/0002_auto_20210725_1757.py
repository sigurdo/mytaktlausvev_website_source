# Generated by Django 3.0.2 on 2021-07-25 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['title']},
        ),
    ]
