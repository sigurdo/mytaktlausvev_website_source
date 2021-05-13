"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from . import views
from . import fetchEndpoints

urlpatterns = [
    path("", views.ScoreList.as_view(), name="sheetmusic"),
    path("score/view/<slug:pk>", views.ScoreView.as_view(), name="viewScore"),
    path("score/edit/<slug:pk>", views.ScoreUpdate.as_view(), name="editScore"),
    path("score/edit/<slug:pk>/parts", views.PartsUpdate.as_view(), name="editScoreParts"),
    path("score/edit/<slug:pk>/parts/create", views.PartCreate.as_view(), name="createScorePart"),
    path("score/edit/<slug:pk>/pdfs", views.PdfsUpdate.as_view(), name="editScorePdfs"),
    path("score/create/", views.ScoreCreate.as_view(), name="createScore"),
    path("score/delete/<int:score_id>", views.deleteScore, name="deleteScore"),
    path("fetch/score", fetchEndpoints.score, name="fetchScore"),
    path("fetch/score/<int:score_id>", fetchEndpoints.score, name="fetchScoreId"),
    path("fetch/pdf/", fetchEndpoints.pdf, name="fetchPdf"),
    path("fetch/pdf/<int:pk>", fetchEndpoints.pdf, name="fetchPdfPk"),
    path("fetch/pdf/processingstatus/<int:pk>", fetchEndpoints.pdfProcessingStatus, name="fetchPdfProcessingStatus"),
    path("fetch/part/", fetchEndpoints.part, name="fetchPart"),
    path("fetch/part/<int:pk>", fetchEndpoints.part, name="fetchPartPk"),
]
