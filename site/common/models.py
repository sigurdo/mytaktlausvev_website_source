from django.db import models
from django.conf import settings


class Page(models.Model):
    title = models.CharField("tittel", max_length=255)
    description = models.TextField("beskrivelse")
    submitted = models.DateTimeField("lagt ut", auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name="laga av",
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True