from django.db import models


class Song(models.Model):
    title = models.CharField("tittel", max_length=255)
    lyrics = models.TextField("tekst")

    def __str__(self):
        return self.title
