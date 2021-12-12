from datetime import date
from django.db.models import (
    Model,
    DateField,
    ForeignKey,
    ImageField,
    CharField,
    CASCADE,
)
from django.urls.base import reverse
from common.models import ArticleMixin
from autoslug.fields import AutoSlugField


class Gallery(ArticleMixin):
    """Model representing a gallery"""

    date = DateField("dato", default=date.today)
    date_to = DateField("til dato", null=True, blank=True)

    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique=True,
        editable=True,
    )

    def get_absolute_url(self):
        return reverse("pictures:GalleryDetail", args=[self.slug])

    class Meta:
        verbose_name = "galleri"
        verbose_name_plural = "galleri"


class Image(Model):
    """Model representing an image in a gallery."""

    gallery = ForeignKey(
        Gallery,
        related_name="images",
        on_delete=CASCADE,
        verbose_name="galleri",
    )
    image = ImageField("bilde")
    description = CharField("beskrivelse", max_length=1024, blank=True)

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url

    class Meta:
        verbose_name = "bilete"
        verbose_name_plural = "bilete"
