# Generated by Django 3.0.2 on 2021-05-12 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sheetmusic', '0006_auto_20210511_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdf',
            name='score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pdfs', to='sheetmusic.Score'),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
