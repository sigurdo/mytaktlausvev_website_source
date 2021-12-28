# Generated by Django 4.0 on 2021-12-27 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uniforms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JacketUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_owner', models.BooleanField(default=True, verbose_name='er eigar')),
                ('jacket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jacket_users', to='uniforms.jacket', verbose_name='jakke')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jacket_users', to='accounts.usercustom', verbose_name='brukar')),
            ],
            options={
                'verbose_name': 'Jakkebrukar',
                'verbose_name_plural': 'Jakkebrukarar',
                'ordering': ['user'],
            },
        ),
        migrations.AddConstraint(
            model_name='jacketuser',
            constraint=models.UniqueConstraint(condition=models.Q(('is_owner', True)), fields=('jacket',), name='one_owner_per_jacket'),
        ),
        migrations.AddConstraint(
            model_name='jacketuser',
            constraint=models.UniqueConstraint(fields=('user',), name='one_jacket_per_user'),
        ),
    ]
