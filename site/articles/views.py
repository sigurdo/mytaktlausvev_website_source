from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Article
from .forms import ArticleForm


class ArticleDetail(DetailView):
    """View for viewing an article."""

    model = Article


class ArticleCreate(PermissionRequiredMixin, CreateView):
    """View for creating a article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/form.html"
    permission_required = "articles.add_article"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    """View for updating a article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/form.html"
    permission_required = "articles.change_article"
