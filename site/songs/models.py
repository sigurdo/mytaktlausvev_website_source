from django.db import models
from django.urls import reverse
from django.conf import settings
from common.models import Page


class Song(Page):
    def get_absolute_url(self):
        return reverse("song_detail", kwargs={"pk": self.pk})

    class Meta(Page.Meta):
        ordering = ["title"]
