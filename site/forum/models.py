from autoslug.fields import AutoSlugField
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import CASCADE, CharField, ForeignKey, Model
from django.urls import reverse

from comments.models import Comment
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
        return Comment.objects.filter(topic__in=self.topics.all()).latest()

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
    posts = GenericRelation(Comment, "object_pk", related_query_name="topic")

    def get_absolute_url(self):
        return reverse("forum:TopicDetail", args=[self.forum.slug, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "emne"
        verbose_name_plural = "emne"
