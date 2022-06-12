from datetime import date

from autoslug import AutoSlugField
from django.db.models import DateField, FileField
from django.urls import reverse

from common.models import ArticleMixin


class Minutes(ArticleMixin):
    date = DateField("dato", default=date.today)
    file = FileField("fil", upload_to="minutes/", default=None, blank=True)
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="title", editable=True, unique=True
    )

    def get_absolute_url(self):
        return reverse("minutes:MinutesDetail", args=[self.slug])

    class Meta:
        ordering = ["-date"]
        verbose_name = "referat"
        verbose_name_plural = "referat"
