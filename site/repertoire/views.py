from django.http import FileResponse
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView

from common.views import FormAndFormsetUpdateView

from .models import Repertoire
from .forms import (
    RepertoireCreateForm,
    RepertoireUpdateForm,
    RepertoireEntryUpdateFormset,
    RepertoireEntryUpdateFormsetHelper,
)


class RepertoireList(LoginRequiredMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"


class RepertoireCreate(PermissionRequiredMixin, CreateView):
    model = Repertoire
    form_class = RepertoireCreateForm
    template_name = "common/form.html"
    permission_required = "repertoire.add_repertoire"

    def get_success_url(self):
        return reverse("repertoire:RepertoireUpdate", args=[self.object.slug])


class RepertoireUpdate(PermissionRequiredMixin, FormAndFormsetUpdateView):
    model = Repertoire
    form_class = RepertoireUpdateForm
    formset_class = RepertoireEntryUpdateFormset
    formset_helper = RepertoireEntryUpdateFormsetHelper
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.change_repertoire"


class RepertoireDelete(PermissionRequiredMixin, DeleteView):
    model = Repertoire
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.delete_repertoire"


class RepertoirePdf(LoginRequiredMixin, DetailView):
    model = Repertoire
    content_type = "application/pdf"

    def render_to_response(self, _):
        pdf_stream = self.get_object().favorite_parts_pdf_file(self.request.user)
        filename = self.get_object().favorite_parts_pdf_filename(self.request.user)
        return FileResponse(
            pdf_stream,
            content_type=self.content_type,
            as_attachment=True,
            filename=filename,
        )
