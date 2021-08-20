from django.urls import reverse
from autoslug import AutoSlugField
from common.models import BaseArticle


class Song(BaseArticle):
    slug = AutoSlugField(
        verbose_name="slug", populate_from="title", unique=True, editable=True
    )

    def get_absolute_url(self):
        return reverse("song_detail", args=[self.slug])

    class Meta(BaseArticle.Meta):
        ordering = ["title"]
