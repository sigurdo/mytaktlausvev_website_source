"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from sheetmusic import views
from sheetmusic import fetchEndpoints

urlpatterns = [
    path("", views.sheetmusic, name="sheetmusic"),
    path("score/view/<int:score_id>", views.viewScore, name="viewScore"),
    path("score/edit/<int:score_id>", views.editScore, name="editScore"),
    path("score/create/", views.createScore, name="createScore"),
    path("score/delete/<int:score_id>", views.deleteScore, name="deleteScore"),
    path("pdf/upload/<int:score_id>/", views.uploadPdf, name="uploadPdf"),
    path("fetch/score", fetchEndpoints.score, name="fetchScore"),
    path("fetch/score/<int:score_id>", fetchEndpoints.score, name="fetchScoreId"),
    path("fetch/pdf/", fetchEndpoints.pdf, name="fetchPdf"),
    path("fetch/pdf/<int:pk>", fetchEndpoints.pdf, name="fetchPdfPk"),
    path("fetch/pdf/processingstatus/<int:pk>", fetchEndpoints.pdfProcessingStatus, name="fetchPdfProcessingStatus"),
    path("fetch/part/", fetchEndpoints.part, name="fetchPart"),
    path("fetch/part/<int:pk>", fetchEndpoints.part, name="fetchPartPk"),
]
