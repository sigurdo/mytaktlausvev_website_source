# Generated by Django 4.1 on 2022-10-05 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_alter_event_created_by_alter_event_modified_by"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventcategory",
            options={
                "ordering": ["name"],
                "verbose_name": "hendingskategori",
                "verbose_name_plural": "hendingskategoriar",
            },
        ),
    ]
