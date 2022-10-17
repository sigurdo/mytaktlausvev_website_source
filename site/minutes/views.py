from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import MinutesForm
from .models import Minutes


def breadcrumbs(minutes=None):
    """Returns breadcrumbs for the minutes views."""
    breadcrumbs = [Breadcrumb(reverse("minutes:MinutesList"), "Alle referat")]
    if minutes:
        breadcrumbs.append(Breadcrumb(minutes.get_absolute_url(), minutes))
    return breadcrumbs


class MinutesList(LoginRequiredMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")


class MinutesDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Minutes

    def get_breadcrumbs(self):
        return breadcrumbs()


class MinutesCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/forms/form.html"

    def get_breadcrumbs(self):
        return breadcrumbs()


class MinutesUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/forms/form.html"
    permission_required = "minutes.change_minutes"

    def get_breadcrumbs(self):
        return breadcrumbs(self.object)


class MinutesDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Minutes
    success_url = reverse_lazy("minutes:MinutesList")
    permission_required = "minutes.delete_minutes"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.object)
