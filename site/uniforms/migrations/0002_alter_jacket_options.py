# Generated by Django 4.0.2 on 2022-02-18 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uniforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jacket',
            options={'ordering': ['number'], 'verbose_name': 'jakke', 'verbose_name_plural': 'jakker'},
        ),
    ]