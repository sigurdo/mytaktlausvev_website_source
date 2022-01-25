from io import BytesIO

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, FormView, ListView
from PyPDF2 import PdfFileReader, PdfFileWriter

from common.views import (
    DeleteViewCustom,
    InlineFormsetCreateView,
    InlineFormsetUpdateView,
)
from sheetmusic.models import Part

from .forms import RepertoireEntryFormset, RepertoireForm, RepertoirePdfFormset
from .models import Repertoire


class RepertoireList(LoginRequiredMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"


class RepertoireCreate(PermissionRequiredMixin, InlineFormsetCreateView):
    model = Repertoire
    form_class = RepertoireForm
    formset_class = RepertoireEntryFormset
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.add_repertoire"


class RepertoireUpdate(PermissionRequiredMixin, InlineFormsetUpdateView):
    model = Repertoire
    form_class = RepertoireForm
    formset_class = RepertoireEntryFormset
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.change_repertoire"


class RepertoireDelete(PermissionRequiredMixin, DeleteViewCustom):
    model = Repertoire
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = "repertoire.delete_repertoire"


class RepertoirePdf(LoginRequiredMixin, FormView, DetailView):
    model = Repertoire
    template_name = "repertoire/repertoire_pdf.html"
    form_class = RepertoirePdfFormset

    def get_initial(self):
        return [
            {
                "score": entry.score,
                "part": entry.score.find_user_part(self.request.user),
            }
            for entry in self.get_object().entries.all()
        ]

    def get_form(self, **kwargs):
        # Here we have to modify the queryset of each subform of the formset
        formset = super().get_form(**kwargs)
        initial = self.get_initial()
        for i, form in enumerate(formset.forms):
            score = initial[i]["score"]
            form.fields["part"].queryset = Part.objects.filter(pdf__score=score)
        return formset

    def form_valid(self, formset):
        pdf_writer = PdfFileWriter()
        for form in formset:
            part = form.cleaned_data["part"]
            pdf_writer.appendPagesFromReader(PdfFileReader(part.pdf_file()))
        output_stream = BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        filename = slugify(f"{self.get_object()} {self.request.user}") + ".pdf"
        return FileResponse(
            output_stream,
            content_type="application/pdf",
            filename=filename,
        )

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Generer PDF for {self.get_object()}"
        return super().get_context_data(**kwargs)
