from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, ListView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import JacketsFormset
from .models import Jacket


class JacketList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Jacket
    context_object_name = "jackets"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("location", "owner")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("uniforms:JacketList"), "Jakkeoversikt")


class JacketsUpdate(PermissionRequiredMixin, BreadcrumbsMixin, FormView):
    form_class = JacketsFormset
    template_name = "common/forms/form.html"
    permission_required = (
        "uniforms.add_jacket",
        "uniforms.change_jacket",
        "uniforms.delete_jacket",
    )
    breadcrumb_parent = JacketList

    def get_success_url(self):
        return reverse("uniforms:JacketList")

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger jakkeoversikt"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # We must explicitly save form since this a FormView and not an UpdateView
        form.save()
        return super().form_valid(form)
