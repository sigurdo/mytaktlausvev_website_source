# Generated by Django 4.0.1 on 2022-01-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_choice_options_choice_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='lagt ut'),
        ),
    ]
