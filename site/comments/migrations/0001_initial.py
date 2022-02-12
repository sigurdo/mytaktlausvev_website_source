# Generated by Django 4.0.2 on 2022-02-12 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('object_pk', models.IntegerField()),
                ('comment', models.TextField(verbose_name='kommentar')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av')),
            ],
            options={
                'verbose_name': 'kommentar',
                'verbose_name_plural': 'kommentarar',
                'ordering': ['created'],
                'get_latest_by': 'created',
            },
        ),
    ]
