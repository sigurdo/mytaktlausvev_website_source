from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count, Max
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Forum, Post, Topic


class ForumList(LoginRequiredMixin, ListView):
    model = Forum
    context_object_name = "forums"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(post_count=Count("topics__posts"))
            .order_by("title")
        )


class TopicList(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = "topics"
    paginate_by = 25

    def setup(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, slug=kwargs["slug_forum"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(forum=self.forum)
            .alias(latest_submitted=Max("posts__submitted", default=F("submitted")))
            .order_by("-latest_submitted")
        )

    def get_context_data(self, **kwargs):
        kwargs["forum"] = self.forum
        return super().get_context_data(**kwargs)


class PostList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 25

    def setup(self, request, *args, **kwargs):
        self.topic = get_object_or_404(
            Topic, slug=kwargs["slug_topic"], forum__slug=kwargs["slug_forum"]
        )
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(topic=self.topic)

    def get_context_data(self, **kwargs):
        kwargs["topic"] = self.topic
        return super().get_context_data(**kwargs)
