"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views
from . import fetchEndpoints

# app_name = "sheetmusic"

urlpatterns = [
    path("", views.ScoreList.as_view(), name="sheetmusic"),
    path("sjåpå/<slug:pk>", views.ScoreView.as_view(), name="ScoreView"),
    path("rediger/<slug:pk>", views.ScoreUpdate.as_view(), name="ScoreUpdate"),
    path(
        "rediger/<slug:pk>/stemmer", views.PartsUpdate.as_view(), name="PartsUpdate"
    ),
    path("rediger/<slug:pk>/pdfar", views.PdfsUpdate.as_view(), name="editScorePdfs"),
    path("rediger/<slug:pk>/pdfar/ny", views.PdfsUpload.as_view(), name="PdfsUpload"),
    path("ny/", views.ScoreCreate.as_view(), name="createScore"),
    path("slett/<slug:pk>", views.ScoreDelete.as_view(), name="ScoreDelete"),
    path("stemme/<slug:pk>/les", views.PartRead.as_view(), name="readPart"),
    path(
        "stemme/<slug:pk>/pdf/<str:filename>", views.PartPdf.as_view(), name="pdfPart"
    ),  # filename is not used for anything, it is just the named the pdf will be saved as at the users machine
    path(
        "favorittstemme",
        fetchEndpoints.usersPreferredPart,
        name="fetchUsersPreferredPart",
    ),
]
