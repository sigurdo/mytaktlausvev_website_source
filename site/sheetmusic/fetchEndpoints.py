""" RESTful APIs for sheetmusic """

import django
from django.contrib.auth.decorators import login_required

# from django.urls import reversed
import json

from sheetmusic.models import Part, UsersPreferredPart


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
