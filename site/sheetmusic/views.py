""" Views for sheetmusic """

import django
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from sheetmusic.models import Score, Pdf
from sheetmusic.forms import CreateScoreForm, UploadPdfForm

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
    if request.method == "POST":
        print("hey ho")
        if not request.user.has_perm("sheetmusic.add_pdf"):
            return django.http.HttpResponseForbidden("Du har ikke retigheter til å laste opp pdfer")
        print("yo")
        print("files:", request.FILES)
        form = UploadPdfForm(request.POST, request.FILES)
        print("formfields:", form.fields)
        print("valid?")
        if form.is_valid():
            print("valid")
            pdf: Pdf = form.save(commit=False)
            pdf.score = Score.objects.get(pk=score_id)
            pdf.timestamp = timezone.now()
            pdf.save()
            print("return")
            return HttpResponseRedirect(reverse("sheetmusic"))
        else:
            print("errors:", form.errors)
            return django.http.HttpResponse(form.errors)
    else:
        return render(request, "sheetmusic/uploadPdfForm.html", { "form": UploadPdfForm() })
