from autoslug.fields import AutoSlugField
from django.db.models import CASCADE, CharField, ForeignKey, Model, TextField
from django.template.defaultfilters import truncatechars
from django.urls import reverse

from common.models import CreatedModifiedMixin


class Forum(Model):
    title = CharField("tittel", max_length=255)
    description = CharField("beskriving", max_length=255)
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


class Topic(CreatedModifiedMixin):
    title = CharField("tittel", max_length=255)
    forum = ForeignKey(
        Forum,
        on_delete=CASCADE,
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


class Post(CreatedModifiedMixin):
    content = TextField("innhald", blank=True)
    topic = ForeignKey(
        Topic,
        on_delete=CASCADE,
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
        ordering = ["created"]
        get_latest_by = "created"
        verbose_name = "innlegg"
        verbose_name_plural = "innlegg"
