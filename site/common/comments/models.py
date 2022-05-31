from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import CASCADE, ForeignKey, IntegerField, TextField

from common.models import CreatedModifiedMixin


class Comment(CreatedModifiedMixin):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_pk = IntegerField()
    content_object = GenericForeignKey("content_type", "object_pk")

    comment = TextField("kommentar")

    def get_absolute_url(self):
        return f"{self.content_object.get_absolute_url()}#comment-{self.pk}"

    def __str__(self):
        stripped = self.comment.rstrip()
        if len(stripped) <= 25:
            return stripped
        return stripped[0:24] + "…"

    class Meta:
        verbose_name = "kommentar"
        verbose_name_plural = "kommentarar"
        ordering = ["created"]
        get_latest_by = "created"
