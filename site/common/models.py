from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)


class CreatedModifiedMixin(Model):
    created = DateTimeField("lagt ut", auto_now_add=True)
    modified = DateTimeField("redigert", auto_now=True)
    created_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="%(class)s_created",
        verbose_name="laga av",
    )
    modified_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="%(class)s_modified",
        verbose_name="redigert av",
    )

    class Meta:
        abstract = True


class ArticleMixin(CreatedModifiedMixin):
    title = CharField("tittel", max_length=255)
    content = TextField("innhald", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
