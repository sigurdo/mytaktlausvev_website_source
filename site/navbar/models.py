from django.contrib.auth.models import Permission
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    FloatField,
    ForeignKey,
    Model,
    TextChoices,
)


class NavbarItem(Model):
    text = CharField(verbose_name="tekst", max_length=255)
    link = CharField(verbose_name="lenkjepeikar", max_length=255, blank=True)
    order = FloatField(verbose_name="rekkjefølgje")
    requires_login = BooleanField(verbose_name="krev innlogging", default=False)

    class Type(TextChoices):
        LINK = "LINK", "Lenkje"
        DROPDOWN = "DROPDOWN", "Nedfallsmeny"

    type = CharField(
        verbose_name="type",
        max_length=255,
        choices=Type.choices,
        default=Type.LINK,
    )
    parent = ForeignKey(
        "self",
        verbose_name="underpunkt av",
        related_name="children",
        blank=True,
        null=True,
        on_delete=SET_NULL,
    )

    def get_sub_items(self):
        return self.children.all()

    def __str__(self):
        match self.type:
            case self.Type.LINK:
                return f"{self.text} ({self.link})"
            case _:
                return f"{self.text} ({self.get_type_display()})"

    class Meta:
        verbose_name = "navigasjonslinepunkt"
        verbose_name_plural = "navigasjonslinepunkt"
        ordering = ["order", "text"]


class NavbarItemPermissionRequirement(Model):
    navbar_item = ForeignKey(
        NavbarItem,
        verbose_name="navigasjonslinepunkt",
        related_name="permission_requirements",
        on_delete=CASCADE,
    )
    permission = ForeignKey(
        Permission,
        verbose_name="løyve",
        related_name="navbar_items",
        on_delete=CASCADE,
    )

    def __str__(self):
        return f"{self.navbar_item} - {self.permission}"

    class Meta:
        verbose_name = "navigasjonslinepunktløyvekrav"
        verbose_name_plural = "navigasjonslinepunktløyvekrav"
