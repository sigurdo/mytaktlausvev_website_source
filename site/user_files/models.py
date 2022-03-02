from django.db.models import CharField, FileField

from common.models import CreatedModifiedMixin


class File(CreatedModifiedMixin):
    name = CharField("namn", max_length=255)
    file = FileField("fil", upload_to="user_files/")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "brukarfil"
        verbose_name_plural = "brukarfiler"
