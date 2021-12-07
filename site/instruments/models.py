from django.db.models import (
    CharField,
    Model,
)


class InstrumentType(Model):
    name = CharField(max_length=255, verbose_name="namn")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "instrumentgruppe"
        verbose_name_plural = "instrumentgrupper"
