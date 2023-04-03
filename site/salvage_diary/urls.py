"""URLs for the 'salvageDiary'-app"""
from django.urls import path

from . import views

app_name = "salvage_diary"

urlpatterns = [
    path("", views.SalvageDiaryEntryList.as_view(), name="SalvageDiaryEntryList"),
    path(
        "<slug:slug>/nytt-innlegg/",
        views.SalvageDiaryEntryCreate.as_view(),
        name="SalvageDiaryEntryCreate",
    ),
    #path("maskoter/", views.MascotList.as_view(), name="MascotList"),
    #path("maskoter/ny/", views.MascotCreate.as_view(), name="MascotCreate"),
    #path("maskot/<int:pk>/rediger/", views.MascotUpdate.as_view, name="MascotUpdate"),
    # "<slug:slug_salvageDiaryEntry>/" - berginger kun på enkeltmaskoter
]
