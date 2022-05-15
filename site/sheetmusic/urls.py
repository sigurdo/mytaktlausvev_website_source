"""Urls for the 'sheetmusic'-app"""
from django.urls import path

from . import views

app_name = "sheetmusic"

urlpatterns = [
    path("", views.ScoreList.as_view(), name="ScoreList"),
    path("ny/", views.ScoreCreate.as_view(), name="ScoreCreate"),
    path("<slug:slug>/", views.ScoreView.as_view(), name="ScoreView"),
    path("<slug:slug>/pdf/", views.ScorePdf.as_view(), name="ScorePdf"),
    path("<slug:slug>/zip/", views.ScoreZip.as_view(), name="ScoreZip"),
    path("<slug:slug>/rediger/", views.ScoreUpdate.as_view(), name="ScoreUpdate"),
    path("<slug:slug>/rediger/pdfar/", views.PdfsUpdate.as_view(), name="PdfsUpdate"),
    path(
        "<slug:slug>/rediger/pdfar/ny/", views.PdfsUpload.as_view(), name="PdfsUpload"
    ),
    path(
        "<slug:slug>/rediger/stemmer/",
        views.PartsUpdateIndex.as_view(),
        name="PartsUpdateIndex",
    ),
    path(
        "<slug:slug>/rediger/stemmer/alle/",
        views.PartsUpdateAll.as_view(),
        name="PartsUpdateAll",
    ),
    path(
        "<slug:score_slug>/rediger/stemmer/<slug:slug>/",
        views.PartsUpdate.as_view(),
        name="PartsUpdate",
    ),
    path("<slug:slug>/slett/", views.ScoreDelete.as_view(), name="ScoreDelete"),
    path(
        "<slug:slug>/favorittstemme/",
        views.FavoritePartPdf.as_view(),
        name="FavoritePartPdf",
    ),
    path(
        "<slug:score_slug>/stemme/<slug:slug>/",
        views.PartPdf.as_view(),
        name="PartPdf",
    ),
    path(
        "favorittstemme",
        views.FavoritePartUpdate.as_view(),
        name="FavoritePartUpdate",
    ),
]
