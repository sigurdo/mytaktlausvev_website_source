from autoslug import AutoSlugField
from django.conf import settings
from django.db import models

from common.models import ArticleMixin


class Poll(ArticleMixin):
    title = None
    content = None
    question = models.CharField("spørsmål", max_length=50)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="question",
        unique=True,
        editable=True,
    )
    public = models.BooleanField(
        "offentleg",
        help_text="Om avstemminga er open for ålmente.",
        default=False,
    )

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.question

    def total_votes(self):
        return 0

    class Meta:
        ordering = ["-submitted"]
        verbose_name = "avstemming"
        verbose_name_plural = "avstemmingar"


class Choice(models.Model):
    text = models.CharField("tekst", max_length=50)
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="avstemming",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "val"
        verbose_name_plural = "val"


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="val",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="poll_votes",
        verbose_name="brukar",
    )

    def __str__(self):
        pass

    class Meta:
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"
