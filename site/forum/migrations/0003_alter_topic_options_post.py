# Generated by Django 4.0 on 2021-12-22 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_usercustom_jacket'),
        ('forum', '0002_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['posts'], 'verbose_name': 'emne', 'verbose_name_plural': 'emne'},
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='tittel')),
                ('content', models.TextField(verbose_name='innhald')),
                ('submitted', models.DateTimeField(auto_now_add=True, verbose_name='lagt ut')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='redigert')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created', to='accounts.usercustom', verbose_name='laga av')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified', to='accounts.usercustom', verbose_name='redigert av')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.topic', verbose_name='emne')),
            ],
            options={
                'verbose_name': 'innlegg',
                'verbose_name_plural': 'innlegg',
                'ordering': ['submitted'],
            },
        ),
    ]
