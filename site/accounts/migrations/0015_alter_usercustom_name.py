# Generated by Django 4.1 on 2022-08-25 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_alter_usercustom_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercustom",
            name="name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="fullt namn"
            ),
        ),
    ]
