# Generated by Django 3.0.2 on 2020-02-19 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_quote_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'ordering': ['-timestamp']},
        ),
    ]