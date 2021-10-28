""" Views for sheetmusic """

# Other python packages
import django
import os
import io
from django.views.generic.base import TemplateResponseMixin
import yaml
import threading
import multiprocessing
import random
from typing import Any, Dict, Optional, Type
from sheatless import processUploadedPdf
from PyPDF2 import PdfFileReader, PdfFileWriter

# Django packages
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db import transaction, models
from django.forms import BaseModelForm, Form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, FormView, ProcessFormView, UpdateView, DeleteView, FormMixin
from django.utils.decorators import classonlymethod
from django.contrib.auth.models import User

# Modules from other apps


# Modules from this app
from .models import Score, Pdf, Part, UsersPreferredPart
from .forms import (
    ScoreCreateForm,
    UploadPdfForm,
    EditScoreForm,
    EditPartForm,
    EditPartFormSet,
    EditPartFormSetHelper,
    PartCreateForm,
)
from . import forms
from .utils import convertPagesToInputFormat, convertInputFormatToPages


# Simplifies management stuff like deleting output files from the code editor on the host system.
os.umask(0)


class ScoreView(LoginRequiredMixin, DetailView):
    model = Score

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
            part.pdfFilename = "{}_{}.pdf".format(
                part.pdf.score.title, part.name
            ).replace(" ", "_")

        context = super().get_context_data(**kwargs)
        context["pdfs"] = pdfs
        context["parts"] = parts
        return context


class ScoreUpdate(LoginRequiredMixin, UpdateView):
    model = Score
    form_class = EditScoreForm

    def get_success_url(self) -> str:
        return reverse("sheetmusic")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        pdfs = Pdf.objects.filter(score=self.get_object())
        parts = []
        for pdf in pdfs:
            pdf.file.displayname = os.path.basename(pdf.file.name)
            parts.extend(
                Part.objects.filter(pdf=pdf).order_by("fromPage", "toPage", "name")
            )
        print("parts:", parts)
        formset = EditPartFormSet(
            queryset=Part.objects.filter(pdf__in=pdfs).order_by(
                "fromPage", "toPage", "name"
            )
        )
        context = super().get_context_data(**kwargs)
        context["formset"] = formset
        context["helper"] = EditPartFormSetHelper
        context["extraData"] = [
            {
                "pdf": {
                    "url": part.pdf.file.url,
                    "name": os.path.basename(part.pdf.file.name),
                    "page": part.fromPage,
                },
                "part": {"pk": part.pk, "displayname": part.name},
            }
            for part in parts
        ]
        context["pdfs"] = pdfs
        return context


class ScoreDelete(LoginRequiredMixin, DeleteView):
    model = Score
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("sheetmusic")


class PartsUpdate(LoginRequiredMixin, FormMixin, SingleObjectMixin, TemplateResponseMixin, ProcessFormView):
    model = Score
    form_class = EditPartFormSet
    template_name = "sheetmusic/parts_update.html"

    def get_success_url(self) -> str:
        return reverse("editScoreParts", args=[self.get_object().pk])

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(
            pdf__score=self.get_object()
        )
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


class PdfsUpdate(LoginRequiredMixin, FormView):
    form_class = UploadPdfForm
    template_name = "sheetmusic/pdfs_update.html"
    success_url = reverse_lazy("sheetmusic")
    context_object_name = "score"

    def get_object(self):
        return Score.objects.get(pk=self.kwargs["pk"])

    def get_success_url(self) -> str:
        return reverse("editScorePdfs", args=[self.get_object().pk])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_object()
        pdfs = Pdf.objects.filter(score=self.get_object())
        for pdf in pdfs:
            pdf.file.displayname = os.path.basename(pdf.file.name)
        context["pdfs"] = pdfs
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        files = self.request.FILES.getlist("files")
        pdfs = []
        for file in files:
            score = Score.objects.get(pk=self.kwargs["pk"])
            pdf = Pdf.objects.create(score=score, file=file)
            pdf.save()
            pdfs.append(pdf)
        processPdfsThread = threading.Thread(target=self.processPdfs, args=[pdfs])
        processPdfsThread.start()
        return super().form_valid(form)

    def processPdfs(self, pdfs):
        for pdf in pdfs:
            pdf.processing = True
            pdf.save()
            try:
                imagesDirPath = os.path.join(
                    django.conf.settings.MEDIA_ROOT, "sheetmusic", "images"
                )
                if not os.path.exists(imagesDirPath):
                    os.mkdir(imagesDirPath)
                imagesDirPath = os.path.join(imagesDirPath, str(pdf.pk))
                if not os.path.exists(imagesDirPath):
                    os.mkdir(imagesDirPath)

                print("skal prøve:", pdf.file.path, imagesDirPath)
                # Gjør dette i en egen prosess for å ikke påvirke responstida på andre requests som må besvares i mellomtida:
                parts, instrumentsDefaultParts = multiprocessing.Pool().apply(
                    processUploadedPdf,
                    (pdf.file.path, imagesDirPath),
                    {
                        "use_lstm": True,
                        "tessdata_dir": os.path.join("tessdata", "tessdata_best-4.1.0"),
                    },
                )
                print("Result:", parts, instrumentsDefaultParts)
                for part in parts:
                    part = Part(
                        name=part["name"],
                        pdf=pdf,
                        fromPage=part["fromPage"],
                        toPage=part["toPage"],
                        timestamp=timezone.now(),
                    )
                    part.save()
            finally:
                pdf.processing = False
                pdf.save()


class ScoreCreate(LoginRequiredMixin, CreateView):
    model = Score
    form_class = ScoreCreateForm
    template_name_suffix = "_create_form"

    def get_success_url(self) -> str:
        return reverse("sheetmusic")


class ScoreList(ListView):
    model = Score
    context_object_name = "scores"

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


class PartCreate(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartCreateForm

    def get_success_url(self) -> str:
        return reverse("editScoreParts", args=[self.object.pdf.score.pk])


class PartRead(LoginRequiredMixin, DetailView):
    model = Part
    template_name = "sheetmusic/part_read.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["pageUrls"] = [
            "/media/sheetmusic/images/{}/page_{}.jpg".format(obj.pdf.pk, pageNum)
            for pageNum in range(obj.fromPage, obj.toPage + 1)
        ]
        return context


class PartPdf(LoginRequiredMixin, DetailView):
    model = Part
    content_type = "application/pdf"

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
        content = self.split_pdf(obj.pdf.file, obj.fromPage, obj.toPage)
        return HttpResponse(content=content, content_type=self.content_type)


def deleteScore(request, score_id=0):
    if request.method == "POST":
        Score.objects.filter(id=score_id).delete()
        return HttpResponseRedirect(reverse("sheetmusic"))
