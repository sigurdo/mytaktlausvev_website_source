# Generated by Django 4.0.2 on 2022-03-03 00:52

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('name', models.CharField(max_length=255, verbose_name='namn')),
                ('file', models.FileField(upload_to='user_files/', verbose_name='fil')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique=True, verbose_name='lenkjenamn')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av')),
            ],
            options={
                'verbose_name': 'brukarfil',
                'verbose_name_plural': 'brukarfiler',
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
    ]
