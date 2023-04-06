"""URLs for the 'salvageDiary'-app"""
from django.urls import path

from . import views

app_name = "salvage_diary"

urlpatterns = [
    path(
        "", views.SalvageDiaryEntryExternalList.as_view(), name="SalvageDiaryEntryList"
    ),
    path(
        "ekstern/<slug:slug>/nytt-innlegg/",
        views.SalvageDiaryEntryExternalCreate.as_view(),
        name="SalvageDiaryEntryExternalCreate",
    ),
    path(
        "ekstern/<int:pk>/rediger/",
        views.SalvageDiaryEntryExternalUpdate.as_view(),
        name="SalvageDiaryEntryUpdateExternal",
    ),
    path(
        "ekstern/<int:pk>/slett/",
        views.SalvageDiaryEntryExternalDelete.as_view(),
        name="SalvageDiaryEntryDeleteExternal",
    ),
    path(
        "intern/",
        views.SalvageDiaryEntryInternalList.as_view(),
        name="SalvageDiaryEntryListInternal",
    ),
    path(
        "intern/nytt-innlegg/",
        views.SalvageDiaryEntryInternalCreate.as_view(),
        name="SalvageDiaryEntryInternalCreate",
    ),
    path(
        "intern/<int:pk>/rediger/",
        views.SalvageDiaryEntryInternalUpdate.as_view(),
        name="SalvageDiaryEntryUpdateInternal",
    ),
    path(
        "intern/<int:pk>/slett/",
        views.SalvageDiaryEntryInternalDelete.as_view(),
        name="SalvageDiaryEntryDeleteInternal",
    ),
    path("maskotar/", views.MascotList.as_view(), name="MascotList"),
    path("maskotar/ny/", views.MascotCreate.as_view(), name="MascotCreate"),
    path(
        "maskotar/<slug:slug>/rediger/",
        views.MascotUpdate.as_view(),
        name="MascotUpdate",
    ),
    path(
        "maskotar/<slug:slug>/slett/", views.MascotDelete.as_view(), name="MascotDelete"
    ),
]
