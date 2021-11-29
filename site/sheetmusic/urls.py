"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views

app_name = "sheetmusic"

urlpatterns = [
    path("", views.ScoreList.as_view(), name="ScoreList"),
    path("ny/", views.ScoreCreate.as_view(), name="ScoreCreate"),
    path("<int:pk>/", views.ScoreView.as_view(), name="ScoreView"),
    path("<int:pk>/rediger/", views.ScoreUpdate.as_view(), name="ScoreUpdate"),
    path("<int:pk>/rediger/stemmer/", views.PartsUpdate.as_view(), name="PartsUpdate"),
    path("<int:pk>/rediger/pdfar/", views.PdfsUpdate.as_view(), name="PdfsUpdate"),
    path("<int:pk>/rediger/pdfar/ny/", views.PdfsUpload.as_view(), name="PdfsUpload"),
    path("<int:pk>/slett/", views.ScoreDelete.as_view(), name="ScoreDelete"),
    path("stemme/<int:pk>/les", views.PartRead.as_view(), name="PartRead"),
    # filename is not used for anything, it is just the name the pdf will be saved as at the users machine
    path("stemme/<int:pk>/pdf/<str:filename>", views.PartPdf.as_view(), name="PartPdf"),
    path(
        "favorittstemme",
        views.UsersPreferredPartUpdateView.as_view(),
        name="fetchUsersPreferredPart",
    ),
]
