# Generated by Django 3.2.7 on 2021-09-16 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_usercustom_membership_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercustom',
            name='address',
            field=models.TextField(blank=True, verbose_name='adresse'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='fødselsdato'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='home_page',
            field=models.URLField(blank=True, max_length=255, verbose_name='heimeside'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, verbose_name='telefonnummer'),
        ),
        migrations.AddField(
            model_name='usercustom',
            name='student_card_number',
            field=models.CharField(blank=True, help_text='Nummeret på studentkortet ditt. Skriv det inn dersom du vil ha tilgang til instrumentlageret. Nummeret er det som startar med EM.', max_length=255, verbose_name='studentkort-nummer'),
        ),
        migrations.AlterField(
            model_name='usercustom',
            name='membership_period',
            field=models.CharField(blank=True, help_text='Årstal, semester - Årstal, semester. Til dømes "2005, Haust - 2009, Vår" eller "2009, Haust -"', max_length=255, verbose_name='medlemsperiode'),
        ),
        migrations.AlterField(
            model_name='usercustom',
            name='membership_status',
            field=models.CharField(choices=[('ACTIVE', 'Aktiv'), ('INACTIVE', 'Inaktiv'), ('RETIRED', 'Pensjonist'), ('SUPPORT', 'Støttemedlem'), ('HONORARY', 'Æresmedlem')], default='ACTIVE', max_length=30, verbose_name='medlemsstatus'),
        ),
    ]
