# Generated by Django 4.0 on 2021-12-27 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uniforms', '0003_migrate_jacketusers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jacket',
            name='owner',
        ),
    ]