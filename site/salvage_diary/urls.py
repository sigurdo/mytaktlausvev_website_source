"""URLs for the 'salvageDiary'-app"""
from django.urls import path

from . import views

app_name = "salvage_diary"

urlpatterns = [
    path(
        "", views.SalvageDiaryEntryExternalList.as_view(), name="SalvageDiaryEntryList"
    ),
    path(
        "<slug:slug>/nytt-innlegg/",
        views.SalvageDiaryEntryExternalCreate.as_view(),
        name="SalvageDiaryEntryExternalCreate",
    ),
    path(
        "<int:pk>/rediger/",
        views.SalvageDiaryEntryExternalUpdate.as_view(),
        name="SalvageDiaryEntryUpdateExternal",
    ),
    path(
        "<int:pk>/slett/",
        views.SalvageDiaryEntryExternalDelete.as_view(),
        name="SalvageDiaryEntryDeleteExternal",
    ),
    path(
        "taktlause",
        views.SalvageDiaryEntryInternalList.as_view(),
        name="SalvageDiaryEntryListInternal",
    ),
    path(
        "nytt-innlegg/",
        views.SalvageDiaryEntryInternalCreate.as_view(),
        name="SalvageDiaryEntryInternalCreate",
    ),
    path(
        "taktlause/<int:pk>/rediger/",
        views.SalvageDiaryEntryInternalUpdate.as_view(),
        name="SalvageDiaryEntryUpdateInternal",
    ),
    path(
        "taktlause/<int:pk>/slett/",
        views.SalvageDiaryEntryInternalDelete.as_view(),
        name="SalvageDiaryEntryDeleteInternal",
    ),
    path("maskot/", views.MascotList.as_view(), name="MascotList"),
    path("maskot/ny/", views.MascotCreate.as_view(), name="MascotCreate"),
    path("maskot/<int:pk>/rediger/", views.MascotUpdate.as_view(), name="MascotUpdate"),
    path("maskot/<int:pk>/slett/", views.MascotDelete.as_view(), name="MascotDelete"),
]
