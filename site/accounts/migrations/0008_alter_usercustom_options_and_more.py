# Generated by Django 4.0.3 on 2022-05-08 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_usercustom_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercustom',
            options={'permissions': (('view_storage_access', 'Kan sjå lagertilgjenge'), ('edit_storage_access', 'Kan redigere lagertilgjenge'), ('view_image_sharing_consent', 'Kan sjå samtykkje til deling av bilete')), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='usercustom',
            name='image_sharing_consent',
            field=models.CharField(choices=[('YES', 'Ja'), ('GROUP_ONLY', 'Berre gruppebilete'), ('NO', 'Nei'), ('UNKNOWN', 'Ukjent')], default='UNKNOWN', help_text='Om bilete du er med i kan delast på DT sine sosiale medier.', max_length=30, verbose_name='samtykkje til deling av bilete'),
        ),
    ]