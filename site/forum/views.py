from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

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
