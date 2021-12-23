from autoslug.fields import AutoSlugField
from django.db import models
from django.template.defaultfilters import truncatechars

from common.models import ArticleMixin


class Forum(models.Model):
    title = models.CharField("tittel", max_length=255)
    description = models.CharField("innhald", max_length=255)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique=True,
        editable=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "forum"
        verbose_name_plural = "forum"


class Topic(ArticleMixin):
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        verbose_name="forum",
        related_name="topics",
    )
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="title",
        unique=True,
        editable=True,
    )

    class Meta:
        verbose_name = "emne"
        verbose_name_plural = "emne"


class Post(ArticleMixin):
    title = None
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name="emne",
        related_name="posts",
    )

    def content_short(self):
        return truncatechars(self.content, 40)

    def __str__(self):
        return self.content_short()

    class Meta:
        ordering = ["-submitted"]
        verbose_name = "innlegg"
        verbose_name_plural = "innlegg"
