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
    UniqueConstraint,
)


class NavbarItem(Model):
    text = CharField(verbose_name="tekst", max_length=255)
    link = CharField(verbose_name="lenkjepeikar", max_length=255, blank=True)
    order = FloatField(verbose_name="rekkjefølgje", default=0)
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
        limit_choices_to={"type": Type.DROPDOWN},
    )

    def sub_items(self):
        return self.children.all()

    def active(self, request):
        """Returns True if navbar_item is active and False if not."""
        request_path = request.path
        match self.type:
            case NavbarItem.Type.LINK:
                item_paths = [self.link]
            case NavbarItem.Type.DROPDOWN:
                item_paths = [subitem.link for subitem in self.sub_items()]
            case _:
                item_paths = []

        for item_path in item_paths:
            if request_path.startswith(item_path):
                return True
        return False

    def permitted(self, user):
        """
        Returns `True` if `user` is permitted to access this navbar item and `False` if not.
        If the item is a dropdown and `user` does not have permission to any sub-items
        the item is also considered unpermitted for `user`.
        """
        if self.requires_login and not user.is_authenticated:
            return False
        for permission_requirement in self.permission_requirements.all():
            permission = permission_requirement.permission
            permission_string = (
                f"{permission.content_type.app_label}.{permission.codename}"
            )
            if not user.has_perm(permission_string):
                return False
        return self.type == NavbarItem.Type.LINK or any(
            subitem.permitted(user) for subitem in self.sub_items()
        )

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
        constraints = [
            UniqueConstraint(fields=["navbar_item", "permission"], name="unique_navbar_item_permission_requirement")
        ]
