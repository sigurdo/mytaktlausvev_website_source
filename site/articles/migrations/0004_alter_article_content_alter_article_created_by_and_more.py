# Generated by Django 4.0 on 2021-12-22 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_usercustom_jacket'),
        ('articles', '0003_alter_article_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, verbose_name='innhald'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to='accounts.usercustom', verbose_name='laga av'),
        ),
        migrations.AlterField(
            model_name='article',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to='accounts.usercustom', verbose_name='redigert av'),
        ),
    ]