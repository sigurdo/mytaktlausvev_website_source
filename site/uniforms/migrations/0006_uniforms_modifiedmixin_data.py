# Generated by Django 4.1 on 2022-10-09 13:04

from random import uniform
from django.conf import settings
from django.db import migrations


def find_test_user(user_model):
    if settings.DEBUG:
        return user_model.objects.get_or_create(username="test", name="Trine Taktlaus")[
            0
        ]
    else:
        return user_model.objects.get(username="test")


def set_uniform_created_by_modified_by(apps, schema_editor):
    UserCustom = apps.get_model("accounts", "UserCustom")
    Jackets = apps.get_model("uniforms", "Jacket")
    for jacket in Jackets.objects.all():
        test_user = find_test_user(UserCustom)
        jacket.created_by = test_user
        jacket.modified_by = test_user
        if jacket.jacket_users.filter(is_owner=True).exists():
            jacket.user = jacket.jacket_users.get(is_owner=True).user
        if UserCustom.objects.filter(
            jacket_user__jacket=jacket, jacket_user__is_owner=False
        ).exists():
            jacket_users = UserCustom.objects.filter(
            jacket_user__jacket=jacket, jacket_user__is_owner=False
        ).all()
            users = ""

            for user in jacket_users:
                users += user.username + " "
            jacket.comment =  users
        jacket.save()


class Migration(migrations.Migration):

    dependencies = [
        ("uniforms", "0005_jacket_created_jacket_created_by_jacket_modified_and_more"),
    ]

    operations = [
        migrations.RunPython(set_uniform_created_by_modified_by),
    ]
