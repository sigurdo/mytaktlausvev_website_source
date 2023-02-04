# Generated by Django 4.1 on 2023-02-04 08:51

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brew",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="lagt ut"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="redigert"),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="namn"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=True,
                        populate_from="name",
                        unique=True,
                        verbose_name="lenkjenamn",
                    ),
                ),
                (
                    "price_per_liter",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="literpris"
                    ),
                ),
                (
                    "available_for_purchase",
                    models.BooleanField(
                        default=False, verbose_name="tilgjengeleg for kjøp"
                    ),
                ),
                (
                    "OG",
                    models.FloatField(
                        blank=True,
                        help_text="Original Gravity. Tettleiken av sukker i brygget før gjæring. Brukt for å berekne alkoholprosent.",
                        null=True,
                        verbose_name="OG",
                    ),
                ),
                (
                    "FG",
                    models.FloatField(
                        blank=True,
                        help_text="Final Gravity. Tettleiken av sukker i brygget etter gjæring. Brukt for å berekne alkoholprosent.",
                        null=True,
                        verbose_name="FG",
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True, upload_to="brewing/logos/", verbose_name="logo"
                    ),
                ),
                (
                    "created_by",
                    django_userforeignkey.models.fields.UserForeignKey(
                        blank=True,
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="laga av",
                    ),
                ),
                (
                    "modified_by",
                    django_userforeignkey.models.fields.UserForeignKey(
                        blank=True,
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="redigert av",
                    ),
                ),
            ],
            options={
                "verbose_name": "brygg",
                "verbose_name_plural": "brygg",
                "ordering": ["name"],
                "get_latest_by": "created",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="lagt ut"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="redigert"),
                ),
                ("amount", models.IntegerField(verbose_name="beløp")),
                (
                    "comment",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="kommentar"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PURCHASE", "Kjøp"), ("DEPOSIT", "Innbetaling")],
                        max_length=30,
                        verbose_name="type",
                    ),
                ),
                (
                    "brew",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="transactions",
                        to="brewing.brew",
                        verbose_name="brygg",
                    ),
                ),
                (
                    "created_by",
                    django_userforeignkey.models.fields.UserForeignKey(
                        blank=True,
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="laga av",
                    ),
                ),
                (
                    "modified_by",
                    django_userforeignkey.models.fields.UserForeignKey(
                        blank=True,
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_modified",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="redigert av",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brewing_transactions",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="brukar",
                    ),
                ),
            ],
            options={
                "verbose_name": "transaksjon",
                "verbose_name_plural": "transaksjonar",
                "ordering": ["-created"],
                "get_latest_by": "created",
            },
        ),
        migrations.AddConstraint(
            model_name="transaction",
            constraint=models.CheckConstraint(
                check=models.Q(("amount__gt", 0)),
                name="transaction_amount_must_be_positive",
                violation_error_message="Beløpet til ein transaksjon må vere større enn 0.",
            ),
        ),
        migrations.AddConstraint(
            model_name="brew",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("price_per_liter__gt", 0),
                    ("price_per_liter", None),
                    _connector="OR",
                ),
                name="brew_price_per_liter_must_be_positive",
                violation_error_message="Literprisen til eit brygg må vere større enn 0.",
            ),
        ),
        migrations.AddConstraint(
            model_name="brew",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("available_for_purchase", True),
                    ("price_per_liter", None),
                    _negated=True,
                ),
                name="brew_price_required_if_available_for_purchase",
                violation_error_message="Literpris er påkravd om brygget skal vere tilgjengeleg for kjøp.",
            ),
        ),
    ]
