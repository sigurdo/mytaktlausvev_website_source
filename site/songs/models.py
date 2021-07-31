from django.db import models
from django.urls import reverse
from django.conf import settings


class Song(models.Model):
    title = models.CharField("tittel", max_length=255)
    lyrics = models.TextField("tekst")
    submitted = models.DateTimeField("lagt ut", auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="songs",
        verbose_name="laga av",
        null=True,
    )

    def get_absolute_url(self):
        return reverse("song_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
