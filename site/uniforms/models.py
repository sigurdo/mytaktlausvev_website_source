from django.conf import settings
from django.db.models import (
    RESTRICT,
    SET_NULL,
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    Model,
    TextChoices,
    TextField,
    OneToOneField,
    BooleanField,
    UniqueConstraint
)

from common.models import CreatedModifiedMixin
from accounts.models import UserCustom


class JacketLocation(Model):
    name = CharField(max_length=255, verbose_name="namn", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jakkestad"
        verbose_name_plural = "jakkestadar"


class Jacket(CreatedModifiedMixin):
    number = IntegerField(verbose_name="jakkenummer", unique=True)
    comment = TextField(verbose_name="kommentar", blank=True)
    state_comment = TextField(verbose_name="tilstandskommentar", blank=True)

    class State(TextChoices):
        GOOD = "GOOD", "God"
        NEEDS_REPAIR = "NEEDS_REPAIR", "Treng reparasjon"
        UNUSABLE = "UNUSABLE", "Ikkje brukbar"

    state = CharField(
        max_length=255,
        verbose_name="tilstand",
        choices=State.choices,
        default=State.GOOD,
    )

    location = ForeignKey(
        JacketLocation,
        verbose_name="stad",
        related_name="jackets",
        on_delete=RESTRICT,
    )

    owner = OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="eigar",
        related_name="jackets",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )

    def get_state_order(self):
        ordering = ["GOOD", "NEEDS_REPAIR", "UNUSABLE"]
        return ordering.index(self.state)

    def __str__(self):
        return f"Jakke {self.number}"

    class Meta:
        ordering = ["number"]
        verbose_name = "jakke"
        verbose_name_plural = "jakker"
       

class JacketUser(Model):
    user = OneToOneField(
        UserCustom,
        verbose_name="brukar",
        related_name="jacket_user",
        on_delete=CASCADE,
    )
    jacket = ForeignKey(
        Jacket,
        verbose_name="jakke",
        related_name="jacket_users",
        on_delete=CASCADE,
    )
    is_owner = BooleanField(
        verbose_name="er eigar",
        default=True,
    )

    def __str__(self):
        return f"{self.user} - {self.jacket}"

    class Meta:
        verbose_name = "Jakkebrukar"
        verbose_name_plural = "Jakkebrukarar"
        ordering = ["user"]
        constraints = [
            UniqueConstraint(
                name="one_owner_per_jacket",
                fields=["jacket"],
                condition=Q(is_owner=True),
                fields=["user"],
            ),
        ]