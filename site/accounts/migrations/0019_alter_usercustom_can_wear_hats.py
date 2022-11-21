# Generated by Django 4.1 on 2022-11-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0018_usercustom_can_wear_hats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercustom",
            name="can_wear_hats",
            field=models.BooleanField(
                default=False,
                help_text="Har tatt opptaket, og kan difor bruka hattar, og treng ikkje bruka aluminiumsfoliehatt",
                null=True,
                verbose_name="kan bruka hattar",
            ),
        ),
    ]
