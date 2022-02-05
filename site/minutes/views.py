from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from common.mixins import BreadcrumbsMixin, PermissionOrCreatedMixin

from .forms import MinutesForm
from .models import Minutes


def breadcrumbs(minutes=None):
    """Returns breadcrumbs for the minutes views."""
    breadcrumbs = [{"url": reverse("minutes:MinutesList"), "name": "Alle referat"}]
    if minutes:
        breadcrumbs.append({"url": minutes.get_absolute_url(), "name": minutes})
    return breadcrumbs


class MinutesList(LoginRequiredMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50


class MinutesDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Minutes

    def get_breadcrumbs(self):
        return breadcrumbs()


class MinutesCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/form.html"

    def get_breadcrumbs(self):
        return breadcrumbs()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class MinutesUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/form.html"
    permission_required = "minutes.change_minutes"

    def get_breadcrumbs(self):
        return breadcrumbs(self.object)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
