""" Views for sheetmusic """

import django
import os
import yaml
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from sheetmusic.models import Score, Pdf, Part
from sheetmusic.forms import CreateScoreForm, UploadPdfForm

from sheetmusic.sheetmusicEngine.sheeetmusicEngine import processUploadedPdf

@login_required
def viewScore(request: HttpRequest, score_id=None):
    score = Score.objects.get(pk=score_id)
    pdfs = Pdf.objects.filter(score=score)
    parts = []
    for pdf in pdfs:
        pdf.file.displayname = os.path.basename(pdf.file.name)
        parts.extend(Part.objects.filter(pdf=pdf))
    for part in parts:
        part.pdfName = os.path.basename(part.pdf.file.name)
    return render(request, "sheetmusic/viewScore.html", { "score": score, "pdfs": pdfs, "parts": parts })

@login_required
def createScore(request: HttpRequest):
    user = request.user
    """ View function for uploading sheet music """
    if request.method == "POST":
        form = CreateScoreForm(request.POST)
        if not user.has_perm("sheetmusic.add_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å opprette note")
        if form.is_valid():
            score = form.save(commit=False)
            score.timestamp = timezone.now()
            score.save()
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

def uploadPdf(request: HttpRequest, score_id=None):
    form = UploadPdfForm()
    if request.method == "POST":
        if not request.user.has_perm("sheetmusic.add_pdf"):
            return django.http.HttpResponseForbidden("Du har ikke retigheter til å laste opp pdfer")
        form = UploadPdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf: Pdf = form.save(commit=False)
            pdf.score = Score.objects.get(pk=score_id)
            pdf.timestamp = timezone.now()
            pdf.save()
            print(pdf.file.path)

            imagesDirPath = os.path.join(django.conf.settings.MEDIA_ROOT, "sheetmusic", "images")
            if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)
            imagesDirPath = os.path.join(imagesDirPath, str(pdf.pk))
            if not os.path.exists(imagesDirPath): os.mkdir(imagesDirPath)

            instrumentsYamlPath = "site/sheetmusic/sheetmusicEngine/instruments.yaml"
            with open(instrumentsYamlPath, "r") as file:
                instruments = yaml.safe_load(file)
            
            print("skal prøve:", pdf.file.path, imagesDirPath)
            parts, instrumentsDefaultParts = processUploadedPdf(pdf.file.path, imagesDirPath, instruments)
            print("Result:", parts, instrumentsDefaultParts)
            for part in parts:
                part = Part(name=part["name"], pdf=pdf, fromPage=part["fromPage"], toPage=part["toPage"], timestamp=timezone.now())
                part.save()
            return HttpResponseRedirect(reverse("sheetmusic"))
    return render(request, "sheetmusic/uploadPdfForm.html", { "form": form })
