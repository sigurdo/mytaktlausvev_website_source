# Generated by Django 4.0 on 2021-12-22 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_usercustom_jacket'),
        ('events', '0003_alter_eventattendance_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventattendance',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='redigert'),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(blank=True, verbose_name='innhald'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to='accounts.usercustom', verbose_name='laga av'),
        ),
        migrations.AlterField(
            model_name='event',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to='accounts.usercustom', verbose_name='redigert av'),
        ),
    ]
