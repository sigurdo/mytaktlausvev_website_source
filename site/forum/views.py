from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count, Max
from django.db.models.expressions import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, ListView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import TopicCreateForm
from .models import Forum, Topic


class ForumList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Forum
    context_object_name = "forums"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(post_count=Count("topics__posts"))
            .order_by("title")
        )

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(url=reverse("forum:ForumList"), label="Alle forum")


class TopicList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Topic
    context_object_name = "topics"
    paginate_by = 25
    breadcrumb_parent = ForumList

    def setup(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, slug=kwargs["slug_forum"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(forum=self.forum)
            .alias(latest_created=Max("posts__created", default=F("created")))
            .order_by("-latest_created")
        )

    def get_context_data(self, **kwargs):
        kwargs["forum"] = self.forum
        return super().get_context_data(**kwargs)

    @classmethod
    def get_breadcrumb(cls, forum, **kwargs):
        return Breadcrumb(url=forum.get_absolute_url(), label=str(forum))


class TopicCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Topic
    form_class = TopicCreateForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = TopicList

    def setup(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, slug=kwargs["slug_forum"])
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = Topic(title=form.cleaned_data["title"], forum=self.forum)
        self.object.save()
        # Here we can not call super().form_valid(), since it will call form.save() which
        # will fail since the form does not know how to set forum
        return HttpResponseRedirect(self.get_success_url())
    
    def get_breadcrumbs_kwargs(self):
        return {"forum": self.forum}


class TopicDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Topic
    context_object_name = "topic"
    paginate_by = 25
    breadcrumb_parent = TopicList

    def get_queryset(self):
        return super().get_queryset().filter(forum__slug=self.kwargs["slug_forum"])

    def get_breadcrumbs_kwargs(self):
        return {"forum": self.object.forum}
