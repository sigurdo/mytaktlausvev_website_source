""" Views for sheetmusic """

# Official python packages
import io
import os
import threading
import random
import json
from typing import Any, Dict

# Other python packages
from PyPDF2 import PdfFileReader, PdfFileWriter

# Django packages
import django
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.forms import BaseModelForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import (
    CreateView,
    FormView,
    ProcessFormView,
    UpdateView,
    DeleteView,
    FormMixin,
)
from django.utils.text import slugify

# Modules from other apps

# Modules from this app
from .models import Score, Pdf, Part, UsersPreferredPart
from .forms import (
    ScoreForm,
    UploadPdfForm,
    EditPartFormSet,
    EditPartFormSetHelper,
    EditPdfFormset,
    EditPdfFormsetHelper,
)


class ScoreView(PermissionRequiredMixin, DetailView):
    model = Score
    permission_required = "sheetmusic.view_score"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        pdfs = Pdf.objects.filter(score=self.get_object())
        for pdf in pdfs:
            pdf.file.displayname = os.path.basename(pdf.file.name)

        parts = Part.objects.filter(pdf__in=pdfs)
        for part in parts:
            part.pdfName = os.path.basename(part.pdf.file.name)
            count = UsersPreferredPart.objects.filter(
                part=part, user=self.request.user
            ).count()
            part.favorite = True if count > 0 else False
            slug = slugify(f"{part.pdf.score.title}-{part.name}")
            part.pdfFilename = f"{slug}.pdf"

        context = super().get_context_data(**kwargs)
        context["pdfs"] = pdfs
        context["parts"] = parts
        return context


class ScoreUpdate(PermissionRequiredMixin, UpdateView):
    model = Score
    form_class = ScoreForm
    permission_required = "sheetmusic.change_score"

    def get_success_url(self) -> str:
        return reverse("sheetmusic:ScoreUpdate", args=[self.get_object().pk])


class ScoreDelete(PermissionRequiredMixin, DeleteView):
    model = Score
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("sheetmusic:ScoreList")
    permission_required = "sheetmusic.delete_score"


class PartsUpdate(
    PermissionRequiredMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = EditPartFormSet
    template_name = "sheetmusic/parts_update.html"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PartsUpdate", args=[self.get_object().pk])

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf__score=self.get_object())
        return kwargs

    def get_form(self, **kwargs) -> BaseModelForm:
        # Here we have to modify the queryset of each subform of the formset
        formset = super().get_form(**kwargs)
        for form in formset.forms:
            form.fields["pdf"].queryset = self.get_object().pdfs
        return formset

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Here we have to inject the formset helper
        kwargs["helper"] = EditPartFormSetHelper
        return super().get_context_data(**kwargs)


class PdfsUpdate(
    PermissionRequiredMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = EditPdfFormset
    template_name = "sheetmusic/pdfs_update.html"
    context_object_name = "score"
    permission_required = "sheetmusic.delete_pdf"

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PdfsUpdate", args=[self.get_object().pk])

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = self.get_object().pdfs.all()
        return kwargs

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["helper"] = EditPdfFormsetHelper()
        return super().get_context_data(**kwargs)


class PdfsUpload(PermissionRequiredMixin, FormView):
    form_class = UploadPdfForm
    template_name = "sheetmusic/pdfs_upload.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.add_pdf", "sheetmusic.add_part")

    def get_object(self):
        return Score.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PdfsUpload", args=[self.get_object().pk])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs[self.context_object_name] = self.get_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        files = self.request.FILES.getlist("files")
        for file in files:
            score = Score.objects.get(pk=self.kwargs["pk"])
            pdf = Pdf.objects.create(score=score, file=file)
            pdf.save()
            plz_wait = self.request.POST.get("plz_wait", False)
            if plz_wait:
                pdf.find_parts()
            else:
                processPdfsThread = threading.Thread(target=pdf.find_parts)
                processPdfsThread.start()
        return super().form_valid(form)


class ScoreCreate(PermissionRequiredMixin, CreateView):
    model = Score
    form_class = ScoreForm
    template_name_suffix = "_create_form"
    permission_required = "sheetmusic.add_score"

    def get_success_url(self) -> str:
        return reverse("sheetmusic:ScoreList")


class ScoreList(PermissionRequiredMixin, ListView):
    model = Score
    context_object_name = "scores"
    permission_required = "sheetmusic.view_score"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        for score in context["scores"]:
            relations = UsersPreferredPart.objects.filter(
                part__pdf__score=score, user=self.request.user
            )
            if len(relations) > 0:
                score.favoritePart = relations[
                    random.randint(0, len(relations) - 1)
                ].part
        return context


class PartRead(PermissionRequiredMixin, DetailView):
    model = Part
    template_name = "sheetmusic/part_read.html"
    permission_required = "sheetmusic.view_part"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["pageUrls"] = [
            "/media/sheetmusic/images/{}/page_{}.jpg".format(obj.pdf.pk, pageNum)
            for pageNum in range(obj.from_page, obj.to_page + 1)
        ]
        return context


class PartPdf(PermissionRequiredMixin, DetailView):
    model = Part
    content_type = "application/pdf"
    permission_required = "sheetmusic.view_part"

    def split_pdf(self, path, from_page, to_page) -> bytes:
        pdf = PdfFileReader(path)
        pdf_writer = PdfFileWriter()
        for page_nr in range(from_page, to_page + 1):
            pdf_writer.addPage(pdf.getPage(page_nr - 1))
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        return output_stream.getvalue()

    def render_to_response(self, _):
        obj = self.get_object()
        content = self.split_pdf(obj.pdf.file, obj.from_page, obj.to_page)
        return HttpResponse(content=content, content_type=self.content_type)


class UsersPreferredPartUpdateView(PermissionRequiredMixin, View):
    permission_required = (
        "sheetmusic.add_userspreferrepart",
        "sheetmusic.delete_userspreferredpart",
    )

    def post(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        part = Part.objects.get(pk=data["part_pk"])
        relation = UsersPreferredPart(user=user, part=part)
        relation.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(relation))

    def delete(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        part = Part.objects.get(pk=data["part_pk"])
        relations = UsersPreferredPart.objects.filter(user=user, part=part)
        for relation in relations:
            relation.delete()
        return django.http.HttpResponse("deleted")
