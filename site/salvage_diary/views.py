from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import (
    MascotForm,
    SalvageDiaryEntryExternalForm,
    SalvageDiaryEntryExternalUpdateForm,
    SalvageDiaryEntryInternalForm,
)
from .models import Mascot, SalvageDiaryEntryExternal, SalvageDiaryEntryInternal


class MascotList(BreadcrumbsMixin, ListView):
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
    breadcrumb_parent = MascotList
    success_url = reverse_lazy("salvage_diary:MascotList")

    def has_permission(self):
        user = self.request.user
        return (
            user.has_perm("salvage_diary.change_mascot")
            or self.get_object().creators.filter(username=user.username).exists()
        )


class MascotDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Mascot
    breadcrumb_parent = MascotList
    success_url = reverse_lazy("salvage_diary:MascotList")

    def has_permission(self):
        user = self.request.user
        return (
            user.has_perm("salvage_diary.delete_mascot")
            or self.get_object().creators.filter(username=user.username).exists()
        )


class SalvageDiaryEntryExternalList(BreadcrumbsMixin, ListView):
    template_name = "salvage_diary/salvagediaryentryexternal_list.html"
    model = SalvageDiaryEntryExternal
    context_object_name = "salvageDiaryEntries"
    queryset = SalvageDiaryEntryExternal.objects.order_by("-created").select_related(
        "mascot"
    )
    paginate_by = 10

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("salvage_diary:SalvageDiaryEntryList"), "Bergedagbok")


class SalvageDiaryEntryExternalCreate(
    SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = SalvageDiaryEntryExternal
    form_class = SalvageDiaryEntryExternalForm
    template_name = "common/forms/form.html"
    success_message = "Bergedagbokinnlegget blei laga!"
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryList")
    breadcrumb_parent = SalvageDiaryEntryExternalList

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


class SalvageDiaryEntryExternalUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView
):
    model = SalvageDiaryEntryExternal
    form_class = SalvageDiaryEntryExternalUpdateForm
    template_name = "common/forms/form.html"
    permission_required = "salvage_diary.change_salvagediaryentryexternal"
    breadcrumb_parent = SalvageDiaryEntryExternalList
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryList")


class SalvageDiaryEntryExternalDelete(
    PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom
):
    model = SalvageDiaryEntryExternal
    permission_required = "salvage_diary.delete_salvagediaryentryexternal"
    breadcrumb_parent = SalvageDiaryEntryExternalList
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryList")


class SalvageDiaryEntryInternalList(BreadcrumbsMixin, ListView):
    template_name = "salvage_diary/salvagediaryentryinternal_list.html"
    model = SalvageDiaryEntryInternal
    context_object_name = "salvageDiaryEntries"
    queryset = SalvageDiaryEntryInternal.objects.order_by("-created")
    paginate_by = 10

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(
            reverse("salvage_diary:SalvageDiaryEntryListInternal"), "Bergedagbok"
        )


class SalvageDiaryEntryInternalCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = SalvageDiaryEntryInternal
    form_class = SalvageDiaryEntryInternalForm
    template_name = "common/forms/form.html"
    success_message = "Bergedagbokinnlegget blei laga!"
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryListInternal")
    breadcrumb_parent = SalvageDiaryEntryInternalList


class SalvageDiaryEntryInternalUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView
):
    model = SalvageDiaryEntryInternal
    form_class = SalvageDiaryEntryInternalForm
    template_name = "common/forms/form.html"
    permission_required = "salvage_diary.change_salvagediaryentryinternal"
    breadcrumb_parent = SalvageDiaryEntryInternalList
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryListInternal")


class SalvageDiaryEntryInternalDelete(
    PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom
):
    model = SalvageDiaryEntryInternal
    permission_required = "salvage_diary.delete_salvagediaryentryinternal"
    breadcrumb_parent = SalvageDiaryEntryInternalList
    success_url = reverse_lazy("salvage_diary:SalvageDiaryEntryListInternal")
