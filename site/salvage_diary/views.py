from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import MascotForm, SalvageDiaryEntryForm
from .models import Mascot, SalvageDiaryEntry


class MascotList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Mascot
    context_object_name = "mascots"
    queryset = Mascot.objects.order_by("name")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("salvage_diary:MascotList"), "Maskot")


class MascotCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = Mascot
    form_class = MascotForm
    template_name = "common/forms/form.html"
    success_message = "Maskoten blei laga"
    permission_required = "salvage_diary.add_mascot"
    breadcrumb_parent = MascotList
    success_url = reverse_lazy("salvage_diary:MascotList")


class MascotUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Mascot
    form_class = MascotForm
    template_name = "common/forms/form.html"
    permission_required = "salvage_diary.change_mascot"
    breadcrumb_parent = MascotList
    success_url = reverse_lazy("salvage_diary:MascotList")


class MascotDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Mascot
    permission_required = "salvage_diary.delete_mascot"
    breadcrumb_parent = MascotList
    success_url = reverse_lazy("salvage_diary:MascotList")


class SalvageDiaryEntryList(BreadcrumbsMixin, ListView):
    model = SalvageDiaryEntry
    context_object_name = "salvageDiaryEntires"
    queryset = SalvageDiaryEntry.objects.order_by("-date").select_related("mascot")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("salvage_diary:SalvageDiaryEntryList"), "Bergedagbok")


class SalvageDiaryEntryCreate(SuccessMessageMixin, BreadcrumbsMixin, CreateView):
    model = SalvageDiaryEntry
    form_class = SalvageDiaryEntryForm
    template_name = "common/forms/form.html"
    success_message = "Bergedagbokinnlegget blei laga!"
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryList")
    breadcrumb_parent = SalvageDiaryEntryList

    mascot = None

    def get_mascot(self):
        if not self.mascot:
            self.mascot = get_object_or_404(Mascot, slug=self.kwargs["slug"])
        return self.mascot

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["mascot"] = self.get_mascot()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["mascot"] = self.get_mascot()
        return super().get_context_data(**kwargs)
