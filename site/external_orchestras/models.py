from django.db.models import CharField, ImageField, Model, TextChoices


class Orchestra(Model):
    class OrchestraCities(TextChoices):
        TRONDHEIM = "TRONDHEIM", "Trondheim"
        AAS = "ÅS", "Ås"
        OSLO = "OSLO", "Oslo"
        KRISTIANSAND = "KRISTIANSAND", "Kristiansand"
        BERGEN = "BERGEN", "Bergen"
        TROMSO = "TROMSØ", "Tromsø"

    name = CharField("namn", max_length=255)
    city = CharField("by", choices=OrchestraCities.choices, blank=True, max_length=255)
    logo = ImageField("logo", upload_to="orchestras/", blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "orchester"
        verbose_name_plural = "orchester"
