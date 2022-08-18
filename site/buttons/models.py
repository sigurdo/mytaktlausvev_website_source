from autoslug import AutoSlugField
from django.db.models import BooleanField, CharField, ImageField
from django.urls import reverse

from common.models import CreatedModifiedMixin


class ButtonDesign(CreatedModifiedMixin):
    name = CharField("namn", max_length=255, unique=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )
    image = ImageField("bilete", upload_to="pictures/")
    public = BooleanField(
        "offentleg", default=False, help_text="Om buttondesignet er ope for ålmente."
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("buttons:ButtonDesignServe", args=[self.slug])

    class Meta:
        ordering = ["name"]
        verbose_name = "buttonmotiv"
        verbose_name_plural = "buttonmotiv"
