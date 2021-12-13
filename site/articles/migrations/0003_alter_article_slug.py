# Generated by Django 3.2.9 on 2021-11-30 23:41

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique_with=('parent',), verbose_name='lenkjenamn'),
        ),
    ]