from django.db.models import CharField, Model


class Constant(Model):
    name = CharField("namn", max_length=255, unique=True)
    value = CharField("verdi", max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "konstant"
        verbose_name_plural = "konstantar"
