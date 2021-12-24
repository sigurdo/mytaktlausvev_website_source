from autoslug.fields import AutoSlugField
from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse("forum:TopicList", args=[self.slug])

    def latest_post(self):
        return Post.objects.filter(topic__in=self.topics.all()).latest()

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
        unique_with="forum",
        editable=True,
    )

    def get_absolute_url(self):
        return reverse("forum:PostList", args=[self.forum.slug, self.slug])

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

    def get_absolute_url(self):
        return reverse("forum:PostList", args=[self.topic.forum.slug, self.topic.slug])

    class Meta:
        ordering = ["submitted"]
        get_latest_by = "submitted"
        verbose_name = "innlegg"
        verbose_name_plural = "innlegg"
