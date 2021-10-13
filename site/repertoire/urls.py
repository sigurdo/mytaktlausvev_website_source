"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RepertoireList.as_view(), name="repertoire"),
    path("nytt", views.RepertoireCreate.as_view(), name="createRepertoire"),
    path("endre/<slug:pk>", views.RepertoireUpdate.as_view(), name="updateRepertoire"),
]
