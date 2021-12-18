from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.CharField(max_length=64)
    content_object = GenericForeignKey("content_type", "object_pk")

    comment = models.TextField("kommentar")
    submitted = models.DateTimeField("lagt ut", auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="laga av",
    )

    def get_absolute_url(self):
        return f"{self.content_object.get_absolute_url()}#comment-{self.pk}"

    def __str__(self):
        stripped = self.comment.rstrip()
        if len(stripped) <= 20:
            return stripped
        return stripped[0:19] + "…"

    class Meta:
        verbose_name = "kommentar"
        verbose_name_plural = "kommentarar"
