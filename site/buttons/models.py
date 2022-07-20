from datetime import date

from autoslug import AutoSlugField
from django.db.models import CharField, ImageField
from django.urls import reverse

from common.models import CreatedModifiedMixin


class ButtonDesign(CreatedModifiedMixin):
    name = CharField("namn", max_length=255, unique=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )
    image = ImageField("bilete", upload_to="pictures/")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "buttonmotiv"
        verbose_name_plural = "buttonmotiv"
