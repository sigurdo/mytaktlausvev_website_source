from django.db.models import (
    Model,
    CharField,
    URLField,
    FloatField,
    TextChoices,
    ForeignKey,
    SET_NULL,
)


class NavbarItem(Model):
    text = CharField(verbose_name="tekst", max_length=255)
    link = CharField(verbose_name="lenkjepeikar", max_length=255)
    order = FloatField(verbose_name="rekkjefølgje")

    class Type(TextChoices):
        LINK = "LINK", "lenkje"
        DROPDOWN = "DROPDOWN", "nedfallsmeny"

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
            # case NavbarItemType.DROPDOWN:
            #     return f"{self.text} (nedfallsmeny)"
            case _:
                return f"{self.text} ({self.type})"

    class Meta:
        verbose_name = "navigasjonslinepunkt"
        verbose_name_plural = "navigasjonslinepunkt"
        ordering = ["order", "text"]
