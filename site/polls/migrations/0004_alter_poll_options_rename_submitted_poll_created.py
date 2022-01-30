# Generated by Django 4.0.1 on 2022-01-13 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_vote_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'get_latest_by': 'created', 'ordering': ['-created'], 'verbose_name': 'avstemming', 'verbose_name_plural': 'avstemmingar'},
        ),
        migrations.RenameField(
            model_name='poll',
            old_name='submitted',
            new_name='created',
        ),
    ]