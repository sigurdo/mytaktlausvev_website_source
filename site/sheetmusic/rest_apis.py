""" RESTful APIs for sheetmusic """

import django
from django.contrib.auth.decorators import login_required
# from django.urls import reversed
from django.utils import timezone
import json

from sheetmusic.models import Score
from django.contrib.auth.models import User

def score(request: django.http.HttpRequest, score_id=None):
    user = request.user
    if request.method == "GET":
        if not user.has_perm("sheetmusic.view_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å se noter")
        if score_id:
            return django.http.JsonResponse(django.forms.models.model_to_dict(Score.objects.get(id=score_id)))
        return django.http.HttpResponse(django.core.serializers.serialize("json", Score.objects.all()))
    elif request.method == "POST":
        if not user.has_perm("sheetmusic.add_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å opprette note")
        data = json.loads(request.body)
        score = Score(title=data["title"], timestamp=timezone.now())
        score.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(score))
    if request.method == "PUT":
        if not score_id:
            return django.http.HttpResponseBadRequest("Ingen score_id oppgitt")
        if not user.has_perm("sheetmusic.change_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å endre noter")
        data = json.loads(request.body)
        score = Score.objects.get(id=score_id)
        score.title = data["title"]
        score.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(score))
    if request.method == "DELETE":
        if not score_id:
            return django.http.HttpResponseBadRequest("Ingen score_id oppgitt")
        if not user.has_perm("sheetmusic.delete_score"):
            return django.http.HttpResponseForbidden("Du har ikke rettigheter til å slette noter")
        Score.objects.filter(id=score_id).delete()
        return django.http.HttpResponse("deleted")
