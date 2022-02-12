# Generated by Django 4.0.2 on 2022-02-12 11:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdventCalendar',
            fields=[
                ('year', models.IntegerField(primary_key=True, serialize=False, verbose_name='år')),
            ],
            options={
                'verbose_name': 'julekalender',
                'verbose_name_plural': 'julekalendrar',
                'ordering': ['-year'],
            },
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('title', models.CharField(max_length=255, verbose_name='tittel')),
                ('content', models.TextField(blank=True, verbose_name='innhald')),
                ('index', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)], verbose_name='index')),
                ('advent_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='windows', to='advent_calendar.adventcalendar', verbose_name='kalender')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av')),
            ],
            options={
                'verbose_name': 'luke',
                'verbose_name_plural': 'luker',
            },
        ),
        migrations.AddConstraint(
            model_name='window',
            constraint=models.UniqueConstraint(fields=('advent_calendar', 'index'), name='uniqueWindow'),
        ),
    ]
