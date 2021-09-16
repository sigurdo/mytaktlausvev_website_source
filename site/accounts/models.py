from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from autoslug import AutoSlugField


class UserManagerCustom(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if self.filter(username__iexact=username).exists():
            raise ValueError("A user with that username already exists.")
        return super()._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class UserCustom(AbstractUser):
    slug = AutoSlugField(verbose_name="slug", populate_from="username", unique=True)

    first_name = None
    last_name = None
    name = models.CharField("navn", max_length=255, blank=True)
    birthdate = models.DateField("fødselsdato", null=True, blank=True)
    phone_number = models.CharField("telefonnummer", max_length=255, blank=True)
    address = models.TextField("adresse", blank=True)
    home_page = models.URLField("heimeside", max_length=255, blank=True)
    student_card_number = models.CharField(
        "studentkort-nummer",
        max_length=255,
        blank=True,
        help_text=(
            "Nummeret på studentkortet ditt. Skriv det inn dersom "
            "du vil ha tilgang til instrumentlageret. Nummeret er det som startar med EM."
        ),
    )
    # rfid - no-one uses this

    class MembershipStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Aktiv"
        INACTIVE = "INACTIVE", "Inaktiv"
        RETIRED = "RETIRED", "Pensjonist"
        SUPPORT = "SUPPORT", "Støttemedlem"
        HONORARY = "HONORARY", "Æresmedlem"

    membership_status = models.CharField(
        "medlemsstatus",
        max_length=30,
        choices=MembershipStatus.choices,
        default=MembershipStatus.ACTIVE,
    )
    # Maybe standardize this field?
    membership_period = models.CharField(
        "medlemsperiode",
        max_length=255,
        blank=True,
        help_text=(
            "Årstal, semester - Årstal, semester. "
            'Til dømes "2005, Haust - 2009, Vår" eller "2009, Haust -"'
        ),
    )

    objects = UserManagerCustom()

    def get_name(self):
        """Returns `name` if it isn't blank, else `username`."""
        return self.name or self.username

    def get_absolute_url(self):
        return reverse("profile", args=[self.slug])
