# Generated by Django 4.0.1 on 2022-01-24 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0002_alter_instrumentgroup_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='namn')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='instruments.instrumentgroup', verbose_name='instrumentgruppe')),
            ],
            options={
                'verbose_name': 'instrumenttype',
                'verbose_name_plural': 'instrumenttyper',
            },
        ),
    ]