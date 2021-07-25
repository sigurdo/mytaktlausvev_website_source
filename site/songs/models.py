from django.db import models
from django.urls import reverse


class Song(models.Model):
    title = models.CharField("tittel", max_length=255)
    lyrics = models.TextField("tekst")

    def get_absolute_url(self):
        return reverse("song_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
