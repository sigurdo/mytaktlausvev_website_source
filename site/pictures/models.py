from datetime import date

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKey,
    ImageField,
    Model,
)
from django.urls.base import reverse

from common.models import ArticleMixin


class Gallery(ArticleMixin):
    """Model representing a gallery."""

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

    def images_latest(self):
        """Returns this gallery's images ordered by `uploaded`, descending."""
        return self.images.order_by("-uploaded")

    class Meta:
        ordering = ["title"]
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
    image = ImageField("bilete", upload_to="pictures/")
    description = CharField("beskrivelse", max_length=1024, blank=True)
    uploaded = DateTimeField("lasta opp", auto_now_add=True)
    uploaded_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="%(class)s_uploaded",
        verbose_name="lasta opp av",
    )
    order = FloatField(
        "rekkjefølgje",
        default=0,
        help_text=(
            "Definerer rekkjefølgja til bilete. "
            "Bilete med lik rekkjefølgje vert sortert etter tidspunkt for opplasting."
        ),
    )

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super().delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url

    class Meta:
        ordering = ["order", "uploaded"]
        verbose_name = "bilete"
        verbose_name_plural = "bilete"
