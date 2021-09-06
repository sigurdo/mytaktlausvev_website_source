# Generated by Django 3.0.2 on 2021-09-06 07:03

import autoslug.fields
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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='tittel')),
                ('content', models.TextField(verbose_name='innhold')),
                ('submitted', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('public', models.BooleanField(default=False, help_text='Om artikkelen er open for ålmente.', verbose_name='offentleg')),
                ('comments_allowed', models.BooleanField(default=True, verbose_name='open for kommentarar')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique_with=('title', 'parent'), verbose_name='slug')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='articles.Article', verbose_name='parent')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('parent', 'slug'), name='unique_slug'),
        ),
    ]
