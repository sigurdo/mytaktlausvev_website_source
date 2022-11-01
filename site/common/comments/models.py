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

    def truncated(self):
        """
        Returns the comment truncated to 25 characters with an ellipsis.
        Whitespace is stripped before truncation.
        """
        stripped = self.comment.rstrip()
        if len(stripped) <= 25:
            return stripped
        return stripped[0:24] + "…"

    def __str__(self):
        return self.truncated()

    class Meta:
        verbose_name = "kommentar"
        verbose_name_plural = "kommentarar"
        ordering = ["created"]
        get_latest_by = "created"
