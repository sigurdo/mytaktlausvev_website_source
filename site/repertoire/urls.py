"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views

app_name = "repertoire"

urlpatterns = [
    path("", views.RepertoireList.as_view(), name="RepertoireList"),
    path("nytt/", views.RepertoireCreate.as_view(), name="RepertoireCreate"),
    path("<int:pk>/endre/", views.RepertoireUpdate.as_view(), name="RepertoireUpdate"),
    path("<int:pk>/slett/", views.RepertoireDelete.as_view(), name="RepertoireDelete"),
    path("<int:pk>/pdf/", views.RepertoirePdf.as_view(), name="RepertoirePdf"),
]
