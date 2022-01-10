from django.conf import settings
from django.db import models, backends
from django.db.models import Model
import random
from sheatless import predict_parts_in_pdf


class ArticleMixin(models.Model):
    title = models.CharField("tittel", max_length=255)
    content = models.TextField("innhald", blank=True)
    submitted = models.DateTimeField("lagt ut", auto_now_add=True)
    modified = models.DateTimeField("redigert", auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
        verbose_name="laga av",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_modified",
        verbose_name="redigert av",
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
