# Generated by Django 4.0 on 2022-01-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['order', 'text'], 'verbose_name': 'val', 'verbose_name_plural': 'val'},
        ),
        migrations.AddField(
            model_name='choice',
            name='order',
            field=models.FloatField(default=0, help_text='Definerer rekkjefølgja til val. Val med lik rekkjefølgje blir sortert etter namn.', verbose_name='rekkjefølgje'),
        ),
    ]