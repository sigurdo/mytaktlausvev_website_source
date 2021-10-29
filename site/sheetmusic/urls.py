"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views
from . import fetchEndpoints

urlpatterns = [
    path("", views.ScoreList.as_view(), name="sheetmusic"),
    path("score/view/<slug:pk>", views.ScoreView.as_view(), name="viewScore"),
    path("score/edit/<slug:pk>", views.ScoreUpdate.as_view(), name="editScore"),
    path(
        "score/edit/<slug:pk>/parts", views.PartsUpdate.as_view(), name="editScoreParts"
    ),
    path(
        "score/edit/<slug:pk>/parts/create",
        views.PartCreate.as_view(),
        name="createScorePart",
    ),
    path("score/edit/<slug:pk>/pdfs", views.PdfsUpdate.as_view(), name="editScorePdfs"),
    path("score/edit/<slug:pk>/upload", views.PdfsUpload.as_view(), name="PdfsUpload"),
    path("score/create/", views.ScoreCreate.as_view(), name="createScore"),
    path("score/delete/<slug:pk>", views.ScoreDelete.as_view(), name="deleteScore"),
    path("part/read/<slug:pk>", views.PartRead.as_view(), name="readPart"),
    path(
        "part/pdf/<slug:pk>/<str:filename>", views.PartPdf.as_view(), name="pdfPart"
    ),  # filename is not used for anything, it is just the named the pdf will be saved as at the users machine
    path("score/delete/<int:score_id>", views.deleteScore, name="deleteScore"),
    path(
        "fetch/userspreferredpart",
        fetchEndpoints.usersPreferredPart,
        name="fetchUsersPreferredPart",
    ),
]
