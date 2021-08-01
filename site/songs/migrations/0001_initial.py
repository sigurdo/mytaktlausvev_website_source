# Generated by Django 3.0.2 on 2021-07-31 19:05

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
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='tittel')),
                ('description', models.TextField(verbose_name='beskrivelse')),
                ('submitted', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
    ]
