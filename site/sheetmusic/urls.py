"""Urls for the 'sheetmusic'-app"""
from django.urls import path, include
from . import views

app_name = "sheetmusic"

score_edit_patterns = [
    path("", views.ScoreUpdate.as_view(), name="ScoreUpdate"),
    path("stemmer/", views.PartsUpdate.as_view(), name="PartsUpdate"),
    path("pdfar/", views.PdfsUpdate.as_view(), name="PdfsUpdate"),
    path("pdfar/ny/", views.PdfsUpload.as_view(), name="PdfsUpload"),
]

score_patterns = [
    path("", views.ScoreView.as_view(), name="ScoreView"),
    path("rediger/", include(score_edit_patterns)),
    path("slett/", views.ScoreDelete.as_view(), name="ScoreDelete"),
]

part_patterns = [
    path("les", views.PartRead.as_view(), name="PartRead"),
    path(
        "pdf/<str:filename>", views.PartPdf.as_view(), name="PartPdf"
    ),  # filename is not used for anything, it is just the named the pdf will be saved as at the users machine
]

urlpatterns = [
    path("", views.ScoreList.as_view(), name="ScoreList"),
    path("ny/", views.ScoreCreate.as_view(), name="ScoreCreate"),
    path("<int:pk>/", include(score_patterns)),
    path("stemme/<int:pk>/", include(part_patterns)),
    path(
        "favorittstemme",
        views.UsersPreferredPartUpdateView.as_view(),
        name="fetchUsersPreferredPart",
    ),
]
