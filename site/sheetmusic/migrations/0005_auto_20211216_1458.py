# Generated by Django 3.2.10 on 2021-12-16 13:58

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0004_set_null_false'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='file',
            field=models.FileField(default=None, upload_to='sheetmusic/original_pdfs/', validators=[common.validators.FileTypeValidator({'application/pdf': ['.pdf'], 'application/x-bzpdf': ['.pdf'], 'application/x-gzpdf': ['.pdf'], 'application/x-pdf': ['.pdf']})], verbose_name='fil'),
        ),
        migrations.AlterField(
            model_name='score',
            name='sound_file',
            field=models.FileField(blank=True, default=None, upload_to='sheetmusic/sound_files/', validators=[common.validators.FileTypeValidator({'audio/flac': ['.flac'], 'audio/midi': ['.midi', '.mid'], 'audio/mp4': ['.mp4', '.m4a'], 'audio/mpeg': ['.mp3'], 'audio/ogg': ['.ogg']})], verbose_name='lydfil'),
        ),
    ]
