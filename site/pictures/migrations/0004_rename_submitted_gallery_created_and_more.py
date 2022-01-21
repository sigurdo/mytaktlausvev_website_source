# Generated by Django 4.0.1 on 2022-01-15 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pictures', '0003_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='submitted',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='gallery',
            name='content',
            field=models.TextField(blank=True, verbose_name='innhald'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='laga av'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to=settings.AUTH_USER_MODEL, verbose_name='redigert av'),
        ),
    ]
