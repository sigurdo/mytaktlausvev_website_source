""" RESTful APIs for sheetmusic """

import django
from django.contrib.auth.decorators import login_required

# from django.urls import reversed
from django.utils import timezone
import json

from sheetmusic.models import Score, Pdf, Part, UsersPreferredPart
from django.contrib.auth.models import User


def score(request: django.http.HttpRequest, score_id=None):
    user = request.user
    if request.method == "GET":
        if not user.has_perm("sheetmusic.view_score"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å se noter"
            )
        if score_id:
            return django.http.JsonResponse(
                django.forms.models.model_to_dict(Score.objects.get(id=score_id))
            )
        return django.http.HttpResponse(
            django.core.serializers.serialize("json", Score.objects.all())
        )
    elif request.method == "POST":
        if not user.has_perm("sheetmusic.add_score"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å opprette note"
            )
        data = json.loads(request.body)
        score = Score(title=data["title"], timestamp=timezone.now())
        score.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(score))
    if request.method == "PUT":
        if not score_id:
            return django.http.HttpResponseBadRequest("Ingen score_id oppgitt")
        if not user.has_perm("sheetmusic.change_score"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å endre noter"
            )
        data = json.loads(request.body)
        score = Score.objects.get(id=score_id)
        score.title = data["title"]
        score.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(score))
    if request.method == "DELETE":
        if not score_id:
            return django.http.HttpResponseBadRequest("Ingen score_id oppgitt")
        if not user.has_perm("sheetmusic.delete_score"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å slette noter"
            )
        Score.objects.filter(id=score_id).delete()
        return django.http.HttpResponse("deleted")


def pdf(request: django.http.HttpRequest, pk=None):
    user = request.user
    if request.method == "GET":
        return django.http.HttpResponse("Ikke implementert", status=501)
    elif request.method == "POST":
        return django.http.HttpResponse("Ikke implementert", status=501)
    elif request.method == "PUT":
        return django.http.HttpResponse("Ikke implementert", status=501)
    if request.method == "DELETE":
        if not pk:
            return django.http.HttpResponseBadRequest("Ingen pdf_pk oppgitt")
        if not user.has_perm("sheetmusic.delete_pdf"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å slette pdf"
            )
        Pdf.objects.filter(pk=pk).delete()
        return django.http.HttpResponse("deleted")


def pdfProcessingStatus(request: django.http.HttpRequest, pk):
    user = request.user
    if request.method == "GET":
        if not pk:
            return django.http.HttpResponseBadRequest("Ingen pdf_pk oppgitt")
        if not user.has_perm("sheetmusic.get_pdf"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å hente pdf-prosesserings-status"
            )
        try:
            pdf = Pdf.objects.get(pk=pk)
        except Pdf.DoesNotExist:
            return django.http.HttpResponseBadRequest(f"Ingen pdf med pk={pk}")
        return django.http.JsonResponse({"processing": pdf.processing})


def part(request: django.http.HttpRequest, pk=None):
    user = request.user
    if request.method == "GET":
        return django.http.HttpResponse("Ikke implementert", status=501)
    elif request.method == "POST":
        return django.http.HttpResponse("Ikke implementert", status=501)
    elif request.method == "PUT":
        if not pk:
            return django.http.HttpResponseBadRequest("Ingen part_pk oppgitt")
        if not user.has_perm("sheetmusic.change_part"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å endre stemmer"
            )
        try:
            part = Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return django.http.HttpResponseBadRequest(f"Ingen stemme med pk={pk}")
        data = json.loads(request.body)
        for key in data:
            if key == "name":
                part.name = data[key]
            elif key == "fromPage":
                part.fromPage = data[key]
            elif key == "toPage":
                part.toPage = data[key]
            else:
                return django.http.HttpResponseBadRequest(
                    "Ikke implementert", status=501
                )
        part.save()
        return django.http.HttpResponse("updated")
        return django.http.HttpResponse("Ikke implementert", status=501)
    if request.method == "DELETE":
        if not pk:
            return django.http.HttpResponseBadRequest("Ingen part_pk oppgitt")
        if not user.has_perm("sheetmusic.delete_part"):
            return django.http.HttpResponseForbidden(
                "Du har ikke rettigheter til å slette stemmer"
            )
        try:
            part = Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return django.http.HttpResponseBadRequest(
                f"Finner ingen stemme med pk lik {pk}"
            )
        part.delete()
        return django.http.HttpResponse("deleted")


@login_required
def usersPreferredPart(request: django.http.HttpRequest, pk=None):
    user = request.user
    if request.method == "GET":
        return django.http.HttpResponse("Ikke implementert", status=501)
    elif request.method == "POST":
        data = json.loads(request.body)
        part = Part.objects.get(pk=data["part_pk"])
        relation = UsersPreferredPart(user=user, part=part)
        relation.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(relation))
    elif request.method == "PUT":
        return django.http.HttpResponse("Ikke implementert", status=501)
    if request.method == "DELETE":
        data = json.loads(request.body)
        part = Part.objects.get(pk=data["part_pk"])
        relations = UsersPreferredPart.objects.filter(user=user, part=part)
        for relation in relations:
            relation.delete()
        return django.http.HttpResponse("deleted")
