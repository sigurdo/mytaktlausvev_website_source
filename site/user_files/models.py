from autoslug import AutoSlugField
from django.db.models import CharField, FileField
from django.db.models.functions import Lower

from common.models import CreatedModifiedMixin


class File(CreatedModifiedMixin):
    name = CharField("namn", max_length=255)
    file = FileField("fil", upload_to="user_files/")
    slug = AutoSlugField(
        verbose_name="lenkjenamn", populate_from="name", editable=True, unique=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.file.url

    class Meta:
        ordering = [Lower("name")]
        verbose_name = "brukarfil"
        verbose_name_plural = "brukarfiler"
