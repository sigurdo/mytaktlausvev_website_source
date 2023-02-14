from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import MinutesForm
from .models import Minutes


class MinutesList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(url=reverse("minutes:MinutesList"), label="Alle referat")


class MinutesDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Minutes
    breadcrumb_parent = MinutesList

    @classmethod
    def get_breadcrumb(cls, minutes, **kwargs):
        return Breadcrumb(url=minutes.get_absolute_url(), label=str(minutes))


class MinutesCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = MinutesList


class MinutesUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/forms/form.html"
    permission_required = "minutes.change_minutes"
    breadcrumb_parent = MinutesDetail

    def get_breadcrumbs_kwargs(self):
        return {"minutes": self.object}


class MinutesDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Minutes
    success_url = reverse_lazy("minutes:MinutesList")
    permission_required = "minutes.delete_minutes"
    breadcrumb_parent = MinutesDetail

    def get_breadcrumbs_kwargs(self):
        return {"minutes": self.object}
