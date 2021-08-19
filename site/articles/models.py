from django.urls import reverse
from autoslug import AutoSlugField
from common.models import Page


class Article(Page):
    slug = AutoSlugField(
        verbose_name="slug", populate_from="title", unique=True, editable=True
    )

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])
