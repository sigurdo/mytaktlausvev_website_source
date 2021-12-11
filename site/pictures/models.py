from datetime import date
from django.db.models import DateField
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

    class Meta:
        verbose_name = "galleri"
        verbose_name_plural = "galleri"
