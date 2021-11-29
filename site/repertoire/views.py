from django.http.response import HttpResponse
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView

from common.views import FormAndFormsetUpdateView

from . import models
from . import forms


class RepertoireList(LoginRequiredMixin, ListView):
    model = models.Repertoire
    context_object_name = "repertoires"


class RepertoireCreate(PermissionRequiredMixin, CreateView):
    model = models.Repertoire
    form_class = forms.RepertoireCreateForm
    template_name_suffix = "_create_form"
    permission_required = "repertoire.add_repertoire"

    def get_success_url(self) -> str:
        return reverse("repertoire:RepertoireList")


class RepertoireUpdate(PermissionRequiredMixin, FormAndFormsetUpdateView):
    model = models.Repertoire
    form_class = forms.RepertoireUpdateForm
    formset_class = forms.RepertoireEntryUpdateFormset
    formset_helper = forms.RepertoireEntryUpdateFormsetHelper
    template_name_suffix = "_update_form"
    permission_required = "repertoire.change_repertoire"

    def get_success_url(self) -> str:
        return reverse(
            "repertoire:RepertoireUpdate", kwargs={"pk": self.get_object().pk}
        )


class RepertoireDelete(PermissionRequiredMixin, DeleteView):
    model = models.Repertoire
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.delete_repertoire"


class RepertoirePdf(LoginRequiredMixin, DetailView):
    model = models.Repertoire
    content_type = "application/pdf"

    def render_to_response(self, _):
        content = self.get_object().pdf_file(self.request.user)
        return HttpResponse(content=content, content_type=self.content_type)
