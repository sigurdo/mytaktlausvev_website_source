from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, ListView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import JacketsFormset
from .models import Jacket


def breadcrumbs(jacket=None):
    """Returns breadcrumbs for the uniforms views."""
    breadcrumbs = [Breadcrumb(reverse("uniforms:JacketList"), "Jakkeoversikt")]
    if jacket:
        breadcrumbs.append(
            Breadcrumb(
                reverse("uniforms:JacketUsers", args=[jacket.number]), str(jacket)
            )
        )
    return breadcrumbs


class JacketList(LoginRequiredMixin, ListView):
    model = Jacket
    context_object_name = "jackets"


class JacketsUpdate(PermissionRequiredMixin, BreadcrumbsMixin, FormView):
    form_class = JacketsFormset
    template_name = "common/forms/form.html"
    permission_required = (
        "uniforms.add_jacket",
        "uniforms.change_jacket",
        "uniforms.delete_jacket",
    )

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger jakkeoversikt"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # We must explicitly save form since this a FormView and not an UpdateView
        form.save()
        return super().form_valid(form)
