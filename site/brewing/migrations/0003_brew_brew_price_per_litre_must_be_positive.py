# Generated by Django 4.1 on 2023-01-29 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("brewing", "0002_alter_transaction_options"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="brew",
            constraint=models.CheckConstraint(
                check=models.Q(("price_per_litre__gt", 0)),
                name="brew_price_per_litre_must_be_positive",
                violation_error_message="Literprisen til eit brygg må vere positiv.",
            ),
        ),
    ]
