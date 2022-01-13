from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey, TextField

from common.models import CreatedModifiedMixin


class Comment(CreatedModifiedMixin):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_pk = CharField(max_length=64)
    content_object = GenericForeignKey("content_type", "object_pk")

    comment = TextField("kommentar")

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
