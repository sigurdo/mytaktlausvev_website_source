"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views

app_name = "repertoire"

urlpatterns = [
    path("", views.RepertoireList.as_view(), name="RepertoireList"),
    path("nytt", views.RepertoireCreate.as_view(), name="RepertoireCreate"),
    path("endre/<slug:pk>", views.RepertoireUpdate.as_view(), name="RepertoireUpdate"),
    path("slett/<slug:pk>", views.RepertoireDelete.as_view(), name="RepertoireDelete"),
]
