""" Views for sheetmusic """

import django
import os
import yaml
import threading
import multiprocessing
from typing import Any, Dict

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.models import User
from sheetmusic.models import Score, Pdf, Part
from sheetmusic.forms import CreateScoreForm, UploadPdfForm, EditScoreForm, EditPartForm, EditPartFormSet, EditPartFormSetHelper
from sheetmusic.utils import convertPagesToInputFormat, convertInputFormatToPages

from sheetmusic.sheetmusicEngine.sheeetmusicEngine import processUploadedPdf

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
        context["pdfInfoForTable"] = [{ "url": part.pdf.file.url, "name": os.path.basename(part.pdf.file.name), "page": part.fromPage } for part in parts]
        context["pdfs"] = pdfs
        return context

@login_required
def createScore(request: HttpRequest):
    user = request.user
    """ View function for uploading sheet music """
    if request.method == "POST":
        form = CreateScoreForm(request.POST)
        if not user.has_perm("sheetmusic.add_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å opprette note")
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("sheetmusic"))
    elif request.method == "GET":
        form = CreateScoreForm()
        return render(request, "sheetmusic/createScoreForm.html", { "form": form })

def sheetmusic(request):
    """ View-function for sheetmusic overview """
    print("Hey hey ho")
    print(Score.objects.all())
    result = render(
        request,
        "sheetmusic/overview.html",
        {
            "ting": 42,
            "scores": Score.objects.all()
        }
    )
    print("Result:", result)
    return result

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
