"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views

app_name = "sheetmusic"

urlpatterns = [
    path("", views.ScoreList.as_view(), name="ScoreList"),
    path("ny/", views.ScoreCreate.as_view(), name="ScoreCreate"),
    path("<slug:slug>/", views.ScoreView.as_view(), name="ScoreView"),
    path("<slug:slug>/rediger/", views.ScoreUpdate.as_view(), name="ScoreUpdate"),
    path(
        "<slug:slug>/rediger/stemmer/", views.PartsUpdate.as_view(), name="PartsUpdate"
    ),
    path("<slug:slug>/rediger/pdfar/", views.PdfsUpdate.as_view(), name="PdfsUpdate"),
    path(
        "<slug:slug>/rediger/pdfar/ny/", views.PdfsUpload.as_view(), name="PdfsUpload"
    ),
    path("<slug:slug>/slett/", views.ScoreDelete.as_view(), name="ScoreDelete"),
    path(
        "<slug:score_slug>/<slug:slug>/les/", views.PartRead.as_view(), name="PartRead"
    ),
    # filename is not used for anything, it is just the name the pdf will be saved as at the users machine
    path(
        "<slug:score_slug>/<slug:slug>/<str:basefilename>.pdf",
        views.PartPdf.as_view(),
        name="PartPdf",
    ),
    path(
        "favorittstemme",
        views.FavoritePartUpdate.as_view(),
        name="FavoritePartUpdate",
    ),
]
