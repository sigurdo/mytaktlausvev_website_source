# Generated by Django 4.0.2 on 2022-03-08 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercustom',
            name='membership_status',
            field=models.CharField(choices=[('PAYING', 'Betalande'), ('ASPIRANT', 'Aspirant'), ('HONORARY', 'Æresmedlem'), ('RETIRED', 'Pensjonist'), ('INACTIVE', 'Inaktiv')], default='ASPIRANT', max_length=30, verbose_name='medlemsstatus'),
        ),
    ]