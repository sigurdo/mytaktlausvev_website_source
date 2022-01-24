# Generated by Django 4.0.1 on 2022-01-24 09:30

from django.db import migrations, models
import django.db.models.deletion


def delete_parts_without_instrument_type(apps, schema_editor):
    Part = apps.get_model("sheetmusic", "Part")
    Part.objects.filter(instrument_type=None).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0004_alter_instrumentgroup_options_and_more'),
        ('sheetmusic', '0014_alter_part_options_remove_part_name_and_more'),
    ]

    operations = [
        migrations.RunPython(delete_parts_without_instrument_type),
        migrations.AlterField(
            model_name='part',
            name='instrument_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='instruments.instrumenttype', verbose_name='instrumenttype'),
        ),
    ]
