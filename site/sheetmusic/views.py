""" Views for sheetmusic """

import django
import os
import io
from django.views.generic.detail import SingleObjectMixin
import yaml
import threading
import multiprocessing
import random
from typing import Any, Dict, Optional, Type

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
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.utils.decorators import classonlymethod

from django.contrib.auth.models import User
from .models import Score, Pdf, Part, UsersPreferredPart
from .forms import ScoreCreateForm, UploadPdfForm, EditScoreForm, EditPartForm, EditPartFormSet, EditPartFormSetHelper, PartCreateForm
from .utils import convertPagesToInputFormat, convertInputFormatToPages

from sheatless import processUploadedPdf
from PyPDF2 import PdfFileReader, PdfFileWriter

os.umask(0) # Simplifies management stuff like deleting output files from the code editor on the host system.



class ScoreView(LoginRequiredMixin, DetailView):
    model = Score

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        pdfs = Pdf.objects.filter(score=self.get_object())
        for pdf in pdfs:
            pdf.file.displayname = os.path.basename(pdf.file.name)

        parts = Part.objects.filter(pdf__in=pdfs)
        for part in parts:
            part.pdfName = os.path.basename(part.pdf.file.name)
            count = UsersPreferredPart.objects.filter(part=part, user=self.request.user).count()
            part.favorite = True if count > 0 else False
            part.pdfFilename = "{}_{}.pdf".format(part.pdf.score.title, part.name).replace(" ", "_")
        
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
            parts.extend(Part.objects.filter(pdf=pdf).order_by('fromPage', 'toPage', 'name'))
        print("parts:", parts)
        formset = EditPartFormSet(queryset=Part.objects.filter(pdf__in=pdfs).order_by('fromPage', 'toPage', 'name'))
        context = super().get_context_data(**kwargs)
        context["formset"] = formset
        context["helper"] = EditPartFormSetHelper
        context["extraData"] = [{
                "pdf": { "url": part.pdf.file.url, "name": os.path.basename(part.pdf.file.name), "page": part.fromPage },
                "part": { "pk": part.pk, "displayname": part.name }
            } for part in parts]
        context["pdfs"] = pdfs
        return context



class PartsUpdate(LoginRequiredMixin, UpdateView):
    model = Score
    form_class = EditPartFormSet
    template_name = "sheetmusic/parts_update.html"

    def get_success_url(self) -> str:
        return reverse("sheetmusic")
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to make UpdateView work with our formset.
        # self.get_form_kwargs() is called by self.get_form(), which is called by self.post().
        # All these methods are inherited by several parent classes, please read the django source code for details.
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance")
        kwargs["queryset"] = Part.objects.filter(pdf__in=self.get_object().pdfs.all()).order_by('pdf', 'fromPage', 'toPage', 'name')
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # We have to override get_context_data() to inject some custom data for our rendering.
        parts = Part.objects.filter(pdf__in=self.get_object().pdfs.all()).order_by('pdf', 'fromPage', 'toPage', 'name')
        context = super().get_context_data(**kwargs)
        context["helper"] = EditPartFormSetHelper
        context["extraData"] = [{
                "pdf": { "url": part.pdf.file.url, "name": os.path.basename(part.pdf.file.name), "page": part.fromPage },
                "part": { "pk": part.pk, "displayname": part.name }
            } for part in parts]
        form = PartCreateForm()
        form.helper.form_action = reverse("createScorePart", args=[self.get_object().pk])
        form.fields["pdf"].queryset = Pdf.objects.filter(score=self.get_object().pk)
        context.update(createForm=form)
        return context



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
                imagesDirPath = os.path.join(django.conf.settings.MEDIA_ROOT, "sheetmusic", "images")
                if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)
                imagesDirPath = os.path.join(imagesDirPath, str(pdf.pk))
                if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)
                
                print("skal prøve:", pdf.file.path, imagesDirPath)
                # Gjør dette i en egen prosess for å ikke påvirke responstida på andre requests som må besvares i mellomtida:
                parts, instrumentsDefaultParts = multiprocessing.Pool().apply(processUploadedPdf, (pdf.file.path, imagesDirPath), { "use_lstm": True, "tessdata_dir": os.path.join("tessdata", "tessdata_best-4.1.0") })
                print("Result:", parts, instrumentsDefaultParts)
                for part in parts:
                    part = Part(name=part["name"], pdf=pdf, fromPage=part["fromPage"], toPage=part["toPage"], timestamp=timezone.now())
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
            relations = UsersPreferredPart.objects.filter(part__pdf__score=score, user=self.request.user)
            if len(relations) > 0:
                score.favoritePart = relations[random.randint(0, len(relations) - 1)].part
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
        context["pageUrls"] = ["/media/sheetmusic/images/{}/page_{}.jpg".format(obj.pdf.pk, pageNum) for pageNum in range(obj.fromPage, obj.toPage + 1)]
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
        return HttpResponse(
            content=content,
            content_type=self.content_type
        )


def deleteScore(request, score_id=0):
    if request.method == "POST":
        Score.objects.filter(id=score_id).delete()
        return HttpResponseRedirect(reverse("sheetmusic"))



