from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count, Max
from django.db.models.expressions import F
from django.views.generic import DetailView, ListView

from .models import Forum


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


class ForumDetail(LoginRequiredMixin, DetailView):
    model = Forum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = (
            context["forum"]
            .topics.alias(
                latest_submitted=Max("posts__submitted", default=F("submitted"))
            )
            .order_by("-latest_submitted")
        )
        return context
