from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import Http404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from common.breadcrumbs import BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import ArticleForm
from .models import Article


class SlugPathMixin:
    """
    Mixin providing a `get_object()` which finds an object by its slug path.
    Raises a 404 if a matching object can't be found.
    Intented to override `SingleObjectMixin`.
    """

    def get_object(self):
        path = self.kwargs.get("path")
        slug_object = path.split("/")[-1]

        candidates = self.get_queryset().filter(slug=slug_object)
        for candidate in candidates:
            if candidate.path() == path:
                return candidate

        raise Http404(f"Couldn't find and article matching path '{path}'.")


class ArticleDetail(UserPassesTestMixin, BreadcrumbsMixin, SlugPathMixin, DetailView):
    """View for viewing an article."""

    model = Article

    def test_func(self):
        return self.get_object().public or self.request.user.is_authenticated

    def get_breadcrumbs(self) -> list:
        return self.object.breadcrumbs()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["subarticles"] = self.object.children.all()
        else:
            context["subarticles"] = self.object.children.filter(public=True)
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    """View for creating an article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/forms/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class SubarticleCreate(SlugPathMixin, BreadcrumbsMixin, ArticleCreate):
    """View for creating a subarticle."""

    def get_breadcrumbs(self) -> list:
        return self.get_object().breadcrumbs(include_self=True)

    def get_initial(self):
        parent = self.get_object()
        return {
            "parent": parent,
            "public": parent.public,
            "comments_allowed": parent.comments_allowed,
        }


class ArticleUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SlugPathMixin, UpdateView
):
    """View for updating a article."""

    model = Article
    form_class = ArticleForm
    template_name = "common/forms/form.html"
    permission_required = "articles.change_article"

    def get_breadcrumbs(self) -> list:
        return self.object.breadcrumbs(include_self=True)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ArticleDelete(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SlugPathMixin, DeleteViewCustom
):
    model = Article
    permission_required = "articles.delete_article"

    def get_breadcrumbs(self) -> list:
        return self.object.breadcrumbs(include_self=True)

    def get_success_url(self) -> str:
        return (
            self.object.parent.get_absolute_url()
            if self.object.parent
            else reverse("dashboard:Dashboard")
        )
