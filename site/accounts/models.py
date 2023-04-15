from secrets import token_urlsafe

from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Q,
    TextChoices,
    TextField,
    UniqueConstraint,
    URLField,
    Value,
)
from django.db.models.functions import Lower, NullIf
from django.templatetags.static import static
from django.urls import reverse

from external_orchestras.models import Orchestra


class UserManagerCustom(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def active(self):
        """
        Returns only active members.
        Active members include paying members, aspirants,
        and members with `is_active_override` set to `True`.
        """
        return super().filter(
            Q(
                membership_status__in=[
                    UserCustom.MembershipStatus.PAYING,
                    UserCustom.MembershipStatus.ASPIRANT,
                ]
            )
            | Q(is_active_override=True)
        )


class UserCustom(AbstractUser):
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="username", unique=True
    )

    first_name = None
    last_name = None
    name = CharField("fullt namn", max_length=255, blank=True)
    preferred_name = CharField(
        "føretrekt namn",
        max_length=255,
        blank=True,
        help_text="Namnet du føretrekkjer at andre brukar.",
    )
    birthdate = DateField("fødselsdato", null=True, blank=True)
    phone_number = CharField("telefonnummer", max_length=255, blank=True)
    address = TextField("adresse", blank=True)
    home_page = URLField("heimeside", max_length=255, blank=True)

    student_card_number = CharField(
        "studentkort-nummer",
        max_length=255,
        blank=True,
        help_text=(
            "Nummeret på studentkortet ditt. Skriv det inn om "
            "du vil ha tilgang til lageret. Nummeret er det som byrjar med EM."
        ),
    )
    has_storage_access = BooleanField(
        "har lagertilgjenge",
        default=False,
        help_text="Om brukaren har fått tilgjenge til lageret.",
    )

    avatar = ImageField("profilbilde", upload_to="profile/", blank=True)
    instrument_type = ForeignKey(
        "instruments.InstrumentType",
        verbose_name="instrumenttype",
        related_name="users",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    class MembershipStatus(TextChoices):
        PAYING = "PAYING", "Betalande"
        ASPIRANT = "ASPIRANT", "Aspirant"
        HONORARY = "HONORARY", "Æresmedlem"
        RETIRED = "RETIRED", "Pensjonist"
        INACTIVE = "INACTIVE", "Inaktiv"

    membership_status = CharField(
        "medlemsstatus",
        max_length=30,
        choices=MembershipStatus.choices,
        default=MembershipStatus.ASPIRANT,
    )
    # Maybe standardize this field?
    membership_period = CharField(
        "medlemsperiode",
        max_length=255,
        blank=True,
        help_text=(
            "Årstal, semester - Årstal, semester. "
            'Til dømes "2005, Haust - 2009, Vår" eller "2009, Haust -"'
        ),
    )

    light_mode = BooleanField(
        "lys modus",
        default=False,
        help_text="Aktiver lys modus. Lys modus vert ikkje aktivt støtta, og er difor ikkje anbefalt.",
    )

    can_wear_hats = BooleanField(
        "kan bruka hattar",
        null=True,
        default=False,
        help_text="Har teke opptaket, og kan difor bruka hattar, og treng ikkje å bruka aluminiumsfoliehatt",
    )

    class ImageSharingConsent(TextChoices):
        YES = "YES", "Ja"
        GROUP_ONLY = "GROUP_ONLY", "Berre gruppebilete"
        NO = "NO", "Nei"
        UNKNOWN = "UNKNOWN", "Ukjent"

    image_sharing_consent = CharField(
        "samtykkje til deling av bilete",
        max_length=30,
        choices=ImageSharingConsent.choices,
        default=ImageSharingConsent.UNKNOWN,
        help_text="Om bilete du er med i kan delast på våre sosiale medier.",
    )

    calendar_feed_token = CharField(
        "kalenderintegrasjonstoken",
        max_length=255,
        default=token_urlsafe,
        unique=True,
        editable=False,
    )
    calendar_feed_start_date = DateField(
        "startdato for kalenderintegrasjon", null=True, blank=True
    )

    orchestras = ManyToManyField(
        verbose_name="andre orchestermedlemskap",
        to=Orchestra,
        blank=True,
        help_text="Andre studentorchester som du er medlem av",
    )

    is_active_override = BooleanField(
        "overstyring av aktiv status",
        default=False,
        help_text="Overstyrer om eit medlem vert sett på som aktivt. Mellombels løysing fram til statuttane er oppklåra.",
    )

    objects = UserManagerCustom()

    def __str__(self):
        return self.get_preferred_name()

    def get_full_name(self):
        """Returns `name` if it exists, else `username`."""
        return self.name or self.username

    def get_preferred_name(self):
        """
        Returns the user's name in this order, depending on what exists:
        - Preferred name
        - First name and the first letter of the user's last name
        - `username`
        """
        if self.preferred_name:
            return self.preferred_name
        elif self.name:
            names = self.name.split(" ")
            if len(names) == 1:
                return self.name
            return f"{names[0]} {names[-1][0]}"
        return self.username

    def is_active_member(self):
        """
        Returns whether `self` is an active member.
        Active members include paying members, aspirants,
        and members with `is_active_override` set to `True`.
        """
        return (
            self.membership_status
            in [
                UserCustom.MembershipStatus.PAYING,
                UserCustom.MembershipStatus.ASPIRANT,
            ]
            or self.is_active_override
        )

    def get_avatar_url(self):
        """
        Returns a URL to the user's avatar if it exists,
        else the default avatar.
        """
        if self.avatar:
            return self.avatar.url
        else:
            return static("accounts/default-avatar.svg")

    def get_absolute_url(self):
        return reverse("accounts:ProfileDetail", args=[self.slug])

    def get_edit_url(self):
        return reverse("accounts:UserCustomUpdate", args=[self.slug])

    class Meta(AbstractUser.Meta):
        ordering = [Lower(NullIf("name", Value("")), nulls_last=True)]
        constraints = [
            UniqueConstraint(Lower("username"), name="username_case_insensitive")
        ]

        permissions = (
            ("view_storage_access", "Kan sjå lagertilgjenge"),
            ("edit_storage_access", "Kan redigere lagertilgjenge"),
            ("view_image_sharing_consent", "Kan sjå samtykkje til deling av bilete"),
            (
                "view_calendar_feed_settings",
                "Kan sjå innstillinger for kalenderintegrasjon",
            ),
            ("edit_instrument_group_leaders", "Kan redigere instrumentgruppeleiarar"),
        )
