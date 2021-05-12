""" Views for sheetmusic """

import django
import os
import yaml
import threading
import multiprocessing
from typing import Any, Dict, Optional, Type

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db import transaction, models
from django.forms import BaseModelForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import classonlymethod

from django.contrib.auth.models import User
from .models import Score, Pdf, Part
from .forms import ScoreCreateForm, UploadPdfForm, EditScoreForm, EditPartForm, EditPartFormSet, EditPartFormSetHelper
from .utils import convertPagesToInputFormat, convertInputFormatToPages

from .sheetmusicEngine.sheeetmusicEngine import processUploadedPdf

class ScoreView(LoginRequiredMixin, DetailView):
    model = Score

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        pdfs = Pdf.objects.filter(score=self.get_object())
        for pdf in pdfs:
            pdf.file.displayname = os.path.basename(pdf.file.name)

        parts = Part.objects.filter(pdf__in=pdfs)
        for part in parts:
            part.pdfName = os.path.basename(part.pdf.file.name)
        
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
        kwargs["queryset"] = Part.objects.filter(pdf__in=self.get_object().pdfs.all()).order_by('fromPage', 'toPage', 'name')
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # We have to override get_context_data() to inject some custom data for our rendering.
        parts = Part.objects.filter(pdf__in=self.get_object().pdfs.all()).order_by('fromPage', 'toPage', 'name')
        context = super().get_context_data(**kwargs)
        context["helper"] = EditPartFormSetHelper
        context["extraData"] = [{
                "pdf": { "url": part.pdf.file.url, "name": os.path.basename(part.pdf.file.name), "page": part.fromPage },
                "part": { "pk": part.pk, "displayname": part.name }
            } for part in parts]
        return context

class PdfsUpdate(LoginRequiredMixin, UpdateView):
    model = Score
    form_class = UploadPdfForm
    template_name = "sheetmusic/pdfs_update.html"

    def get_success_url(self) -> str:
        return reverse("sheetmusic")

    # @classonlymethod
    # def as_view(cls, **initkwargs):
    #     def view(request, *args, **kwargs):
    #         self = cls(**initkwargs)
    #         print("request:", request)
    #         print("args:", args)
    #         print("kwargs:", kwargs)
    #         self.score_pk = kwargs["pk"]
    #         kwargs.pop("pk")
    #         self.setup(request, *args, **kwargs)
    #         if not hasattr(self, 'request'):
    #             raise AttributeError(
    #                 "%s instance has no 'request' attribute. Did you override "
    #                 "setup() and forget to call super()?" % cls.__name__
    #             )
    #         return self.dispatch(request, *args, **kwargs)
    #     return view

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to make UpdateView work with our formset.
        # self.get_form_kwargs() is called by self.get_form(), which is called by self.post().
        # All these methods are inherited by several parent classes, please read the django source code for details.
        kwargs = super().get_form_kwargs()
        # kwargs.pop("instance")
        kwargs["instance"] = Pdf.objects.filter(score=self.get_object())[0]
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        print("getting context data")
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        pdf: Pdf = form.save(commit=False)
        pdf.score = Score.objects.get(pk=2)
        pdf.timestamp = timezone.now()
        pdf.save()
        print(pdf.file.path)

        pdf.processing = True
        pdf.save()
        processPdfThread = threading.Thread(target=processPdf, args=[pdf])
        processPdfThread.start()
        print("form valid:", form)
        # res = form.save()
        print("form saved")
        return super().form_valid(form)

class ScoreCreate(LoginRequiredMixin, CreateView):
    model = Score
    form_class = ScoreCreateForm
    template_name_suffix = "_create_form"

    def get_success_url(self) -> str:
        return reverse("sheetmusic")

class ScoreList(ListView):
    model = Score

def deleteScore(request, score_id=0):
    if request.method == "POST":
        Score.objects.filter(id=score_id).delete()
        return HttpResponseRedirect(reverse("sheetmusic"))

def processPdf(pdf: Pdf):
    pdf.processing = True
    pdf.save()
    try:
        imagesDirPath = os.path.join(django.conf.settings.MEDIA_ROOT, "sheetmusic", "images")
        if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)
        imagesDirPath = os.path.join(imagesDirPath, str(pdf.pk))
        if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)

        instrumentsYamlPath = "site/sheetmusic/sheetmusicEngine/instruments.yaml"
        with open(instrumentsYamlPath, "r") as file:
            instruments = yaml.safe_load(file)
        
        print("skal prøve:", pdf.file.path, imagesDirPath)
        # Gjør dette i en egen prosess for å ikke påvirke responstida på andre requests som må besvares i mellomtida:
        parts, instrumentsDefaultParts = multiprocessing.Pool().apply(processUploadedPdf, (pdf.file.path, imagesDirPath, instruments))
        print("Result:", parts, instrumentsDefaultParts)
        for part in parts:
            part = Part(name=part["name"], pdf=pdf, fromPage=part["fromPage"], toPage=part["toPage"], timestamp=timezone.now())
            part.save()
    finally:
        pdf.processing = False
        pdf.save()

def uploadPdf(request: HttpRequest, score_id=None):
    form = UploadPdfForm()
    if request.method == "POST":
        if not request.user.has_perm("sheetmusic.add_pdf"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å laste opp pdfer")
        form = UploadPdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf: Pdf = form.save(commit=False)
            pdf.score = Score.objects.get(pk=score_id)
            pdf.timestamp = timezone.now()
            pdf.save()
            print(pdf.file.path)

            pdf.processing = True
            pdf.save()
            processPdfThread = threading.Thread(target=processPdf, args=[pdf])
            processPdfThread.start()
            
            return HttpResponseRedirect(reverse("editScore", args=[score_id]))
    return render(request, "sheetmusic/uploadPdfForm.html", { "form": form })
