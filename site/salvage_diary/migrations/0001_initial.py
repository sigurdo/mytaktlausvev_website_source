# Generated by Django 4.1 on 2023-04-05 20:25

import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
import django_userforeignkey.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("events", "0012_eventattendance_instrument_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mascot",
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
                ("name", models.CharField(max_length=255, verbose_name="namn")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="salvage_diary/mascots/",
                        verbose_name="bilete",
                    ),
                ),
                (
                    "creation_start_date",
                    models.DateField(
                        blank=True,
                        help_text="Når starta laginga av maskoten?",
                        null=True,
                        verbose_name="startdato",
                    ),
                ),
                (
                    "creation_end_date",
                    models.DateField(
                        blank=True,
                        help_text="Når vert maskoten ferdig?",
                        null=True,
                        verbose_name="sluttdato",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True,
                        help_text="Dette er eit passord me festar på maskoten under hendinga som bergarne må fylla inn i skjemaet for å forsikra oss om at dei har berga maskoten.",
                        max_length=255,
                        verbose_name="passord",
                    ),
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
                ("note", models.TextField(blank=True, verbose_name="Notat")),
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
                    "creators",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL, verbose_name="Skapere"
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
                "verbose_name": "maskot",
                "verbose_name_plural": "maskotar",
            },
        ),
        migrations.CreateModel(
            name="SalvageDiaryEntryInternal",
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
                ("title", models.CharField(max_length=255, verbose_name="tittel")),
                (
                    "thieves",
                    models.CharField(
                        blank=True,
                        help_text="Kven er dykk?",
                        max_length=255,
                        verbose_name="bergere",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Ønskjer du fleire bilete, lag fleire innlegg",
                        upload_to="salvage_diary/pictures",
                        verbose_name="bilete",
                    ),
                ),
                (
                    "story",
                    models.TextField(
                        blank=True,
                        help_text="Kva skjedde? Korleis berga dykk den? Kva har dykk endra?",
                        verbose_name="Historie",
                    ),
                ),
                (
                    "item",
                    models.CharField(
                        help_text="Kva ble berga?",
                        max_length=255,
                        verbose_name="objekt",
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
                    "event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="salvageDiaryEntries",
                        to="events.event",
                        verbose_name="hending",
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
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Vel taktlause medlemmer som var involverte i berginga. Vil ikkje vises om 'Bergere' er fylt ut",
                        related_name="salvageDiaryEntries",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="involverte medlemmar",
                    ),
                ),
            ],
            options={
                "verbose_name": "bergedagbokinnlegg - DT",
                "verbose_name_plural": "bergedagbokinnlegg - DT",
            },
        ),
        migrations.CreateModel(
            name="SalvageDiaryEntryExternal",
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
                ("title", models.CharField(max_length=255, verbose_name="tittel")),
                (
                    "thieves",
                    models.CharField(
                        blank=True,
                        help_text="Kven er dykk?",
                        max_length=255,
                        verbose_name="bergere",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Ønskjer du fleire bilete, lag fleire innlegg",
                        upload_to="salvage_diary/pictures",
                        verbose_name="bilete",
                    ),
                ),
                (
                    "story",
                    models.TextField(
                        blank=True,
                        help_text="Kva skjedde? Korleis berga dykk den? Kva har dykk endra?",
                        verbose_name="Historie",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="tidspunkt"
                    ),
                ),
                (
                    "event",
                    models.CharField(
                        blank=True,
                        help_text="Når skjedde dette? SMASH? TORSK? Medaljegalla?",
                        max_length=255,
                        verbose_name="hending",
                    ),
                ),
                (
                    "mascot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="salvageEntries",
                        to="salvage_diary.mascot",
                        verbose_name="maskot",
                    ),
                ),
            ],
            options={
                "verbose_name": "bergedagbokinnlegg",
                "verbose_name_plural": "bergedagbokinnlegg",
            },
        ),
        migrations.AddConstraint(
            model_name="mascot",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("creation_end_date__gte", models.F("creation_start_date")),
                    ("creation_end_date__isnull", True),
                    ("creation_start_date__isnull", True),
                    _connector="OR",
                ),
                name="mascot_start_date_must_be_after_end_date",
                violation_error_message="Så vidt me veit er tidsreiser enno ikkje offentleg tilgjengeleg, så startdatoen kan ikkje vera etter sluttdatoen. \n                Viss du kan reisa i tid, ver vennleg og gi beskjed til vevkom slik at me kan fjerna valideringa.",
            ),
        ),
    ]
