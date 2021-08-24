from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from .models import Article
from .forms import ArticleForm


class ArticleDetail(UserPassesTestMixin, DetailView):
    """View for viewing an article."""

    model = Article

    def get_object(self):
        path = self.kwargs.get("path")
        slug_object = path.split("/")[-1]

        candidates = self.get_queryset().filter(slug=slug_object)
        for candidate in candidates:
            if candidate.path() == path:
                return candidate

    def test_func(self):
        return self.get_object().public or self.request.user.is_authenticated


class ArticleCreate(PermissionRequiredMixin, CreateView):
    """View for creating a article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/form.html"
    permission_required = "articles.add_article"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    """View for updating a article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/form.html"
    permission_required = "articles.change_article"

    def get_object(self):
        path = self.kwargs.get("path")
        slug_object = path.split("/")[-1]

        candidates = self.get_queryset().filter(slug=slug_object)
        for candidate in candidates:
            if candidate.path() == path:
                return candidate

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
