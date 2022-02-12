# Generated by Django 4.0.2 on 2022-02-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionCustom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('view_storage_access', 'Kan sjå lagertilgjenge'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
