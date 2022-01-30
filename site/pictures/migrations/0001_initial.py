# Generated by Django 4.0.1 on 2022-01-23 20:11

import autoslug.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('title', models.CharField(max_length=255, verbose_name='tittel')),
                ('content', models.TextField(blank=True, verbose_name='innhald')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='dato')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='til dato')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True, verbose_name='lenkjenamn')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av')),
            ],
            options={
                'verbose_name': 'galleri',
                'verbose_name_plural': 'galleri',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pictures/', verbose_name='bilete')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='beskrivelse')),
                ('uploaded', models.DateTimeField(auto_now_add=True, verbose_name='lasta opp')),
                ('order', models.FloatField(default=0, help_text='Definerer rekkjefølgja til biletet. Bilete med lik rekkjefølgje vert sortert etter tidspunkt for opplasting.', verbose_name='rekkjefølgje')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pictures.gallery', verbose_name='galleri')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_uploaded', to=settings.AUTH_USER_MODEL, verbose_name='lasta opp av')),
            ],
            options={
                'verbose_name': 'bilete',
                'verbose_name_plural': 'bilete',
                'ordering': ['order', 'uploaded'],
            },
        ),
    ]