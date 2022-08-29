
from django.db.models import (
    CharField,
    ImageField,
    TextChoices,
    Model,
)

class Orchestra(Model):
    class OrchestraCities(TextChoices):
        TRONDHEIM = "TRONDHEIM", "Trondheim"
        AAS = "ÅS", "Ås"
        OSLO = "OSLO", "Oslo"
        KRISTIANSAND = "KRISTIANSAND", "Kristiansand"
        BERGEN = "BERGEN", "Bergen"
        TROMSO = "TROMSØ", "Tromsø"

    name = CharField("Namn", max_length=255)
    city = CharField( "By",
        choices=OrchestraCities.choices,
        blank=True,
        max_length=255
    )
    avatar = ImageField("logo", upload_to="orchestras/", blank=True)

    def __str__(self):
        return f"{self.name}"



    