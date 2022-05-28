from django.db.models import CharField, Model, TextField


class EmbeddableText(Model):
    """
    A piece of text that can be configured in the admin panel.
    Intended to be embedded with a hardcoded `name` in apps that need text that is easy for site admins to update.
    """

    name = CharField("namn", max_length=255, unique=True)
    content = TextField("innhald", blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "innbyggbar tekst"
        verbose_name_plural = "innbyggbare tekster"
