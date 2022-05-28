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
    TextChoices,
    TextField,
    UniqueConstraint,
    URLField,
)
from django.db.models.functions import Lower
from django.templatetags.static import static
from django.urls import reverse


class UserManagerCustom(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def active(self):
        """Returns only active members, which means paying members and aspirants."""
        return super().filter(
            membership_status__in=[
                UserCustom.MembershipStatus.PAYING,
                UserCustom.MembershipStatus.ASPIRANT,
            ]
        )


class UserCustom(AbstractUser):
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="username", unique=True
    )

    first_name = None
    last_name = None
    name = CharField("navn", max_length=255, blank=True)
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
        help_text="Om bilete du er med i kan delast på DT sine sosiale medier.",
    )

    calendar_feed_token = CharField(
        "Kalenderfeedtoken",
        max_length=255,
        default=token_urlsafe,
        unique=True,
        editable=False,
    )
    calendar_feed_only_upcoming = BooleanField(
        "Få kun framtidige hendingar i kalenderfeed", default=True
    )
    calendar_feed_start_date = DateField(
        "Startdato for kalenderfeed", null=True, blank=True
    )

    objects = UserManagerCustom()

    def __str__(self):
        return self.get_name()

    def get_name(self):
        """Returns `name` if it exists, else `username`."""
        return self.name or self.username

    def is_active_member(self):
        """
        Returns whether `self` is an active member.
        Active members include paying members and aspirants.
        """
        return self.membership_status in [
            UserCustom.MembershipStatus.PAYING,
            UserCustom.MembershipStatus.ASPIRANT,
        ]

    def get_avatar_url(self):
        """
        Returns a URL to the user's avatar if it exists,
        else the default avatar.
        """
        if self.avatar:
            return self.avatar.url
        else:
            return static("accounts/default-avatar.svg")

    def get_jacket(self):
        jacket_user = getattr(self, "jacket_user", None)
        if jacket_user:
            return jacket_user.jacket
        return None

    def get_absolute_url(self):
        return reverse("accounts:ProfileDetail", args=[self.slug])

    def get_edit_url(self):
        return reverse("accounts:UserCustomUpdate", args=[self.slug])

    class Meta(AbstractUser.Meta):
        constraints = [
            UniqueConstraint(Lower("username"), name="username_case_insensitive")
        ]

        permissions = (
            ("view_storage_access", "Kan sjå lagertilgjenge"),
            ("edit_storage_access", "Kan redigere lagertilgjenge"),
            ("view_image_sharing_consent", "Kan sjå samtykkje til deling av bilete"),
        )
