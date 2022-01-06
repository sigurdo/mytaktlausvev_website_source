# Generated by Django 4.0 on 2022-01-06 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='tekst')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='lenkjepeikar')),
                ('order', models.FloatField(verbose_name='rekkjefølgje')),
                ('requires_login', models.BooleanField(default=False, verbose_name='krev innlogging')),
                ('type', models.CharField(choices=[('LINK', 'lenkje'), ('DROPDOWN', 'nedfallsmeny')], default='LINK', max_length=255, verbose_name='type')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='navbar.navbaritem', verbose_name='underpunkt av')),
            ],
            options={
                'verbose_name': 'navigasjonslinepunkt',
                'verbose_name_plural': 'navigasjonslinepunkt',
                'ordering': ['order', 'text'],
            },
        ),
        migrations.CreateModel(
            name='NavbarItemPermissionRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navbar_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_requirements', to='navbar.navbaritem', verbose_name='navigasjonslinepunkt')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='navbar_items', to='auth.permission', verbose_name='løyve')),
            ],
            options={
                'verbose_name': 'navigasjonslinepunktløyvekrav',
                'verbose_name_plural': 'navigasjonslinepunktløyvekrav',
            },
        ),
    ]
