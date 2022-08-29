from django.db.models import CASCADE, CharField, DateTimeField, Model, TextField
from django_userforeignkey.models.fields import UserForeignKey


class CreatedModifiedMixin(Model):
    created = DateTimeField("lagt ut", auto_now_add=True)
    modified = DateTimeField("redigert", auto_now=True)
    created_by = UserForeignKey(
        auto_user_add=True,
        on_delete=CASCADE,
        null=False,
        related_name="%(class)s_created",
        verbose_name="laga av",
    )
    modified_by = UserForeignKey(
        auto_user=True,
        on_delete=CASCADE,
        null=False,
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
