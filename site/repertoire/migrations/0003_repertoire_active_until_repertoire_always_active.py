# Generated by Django 4.1 on 2022-08-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repertoire", "0002_alter_repertoireentry_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="repertoire",
            name="active_until",
            field=models.DateField(
                blank=True,
                default=None,
                help_text='Gjer repertoaret aktivt til og med ein bestemt dato. Hugs å ikkje sette "Alltid aktivt"-feltet om repertoaret ikkje skal vere aktivt etter denne datoen.',
                null=True,
                verbose_name="Aktivt til",
            ),
        ),
        migrations.AddField(
            model_name="repertoire",
            name="always_active",
            field=models.BooleanField(default=True, verbose_name="Alltid aktivt"),
        ),
    ]
