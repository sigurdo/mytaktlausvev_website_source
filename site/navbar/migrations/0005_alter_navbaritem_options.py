# Generated by Django 4.0 on 2021-12-31 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navbar', '0004_alter_navbaritem_options_alter_navbaritem_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='navbaritem',
            options={'ordering': ['parent', 'order', 'text'], 'verbose_name': 'navigasjonslinepunkt', 'verbose_name_plural': 'navigasjonslinepunkt'},
        ),
    ]
