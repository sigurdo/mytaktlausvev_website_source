from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

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
    template_name = "common/form.html"
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
            # print("form:", form)
            # print("fields:", form.fields)
            # print("fields:", form.__dict__)
            # # print("part:", form.fields["part"])
            # print("score:", form.fields["score"])
            # print("score:", form.fields["score"].__dict__)
            # print("initial:", initial[i]["score"])
            form.fields["part"].queryset = Part.objects.filter(pdf__score=score)
            # print("sånn")
            # form.fields["part"].queryset = self.get_object().pdfs
        return formset

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Generer PDF for {self.get_object()}"
        return super().get_context_data(**kwargs)

    # content_type = "application/pdf"

    # def render_to_response(self, _):
    #     pdf_stream = self.get_object().favorite_parts_pdf_file(self.request.user)
    #     filename = self.get_object().favorite_parts_pdf_filename(self.request.user)
    #     return FileResponse(
    #         pdf_stream,
    #         content_type=self.content_type,
    #         filename=filename,
    #     )
