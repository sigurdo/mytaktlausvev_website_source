"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from sheetmusic import views
from sheetmusic import rest_apis

urlpatterns = [
    path("", views.sheetmusic, name="sheetmusic"),
    path("score/view/<int:score_id>", views.viewScore, name="viewScore"),
    path("score/edit/<int:score_id>", views.editScore, name="editScore"),
    path("score/create/", views.createScore, name="createScore"),
    path("score/delete/<int:score_id>", views.deleteScore, name="deleteScore"),
    path("pdf/upload/<int:score_id>/", views.uploadPdf, name="uploadPdf"),
    path("rest/score", rest_apis.score, name="scoreRest"),
    path("rest/score/<int:score_id>", rest_apis.score, name="scoreRestId"),
    path("rest/pdf/", rest_apis.pdf, name="pdfRest"),
    path("rest/pdf/<int:pk>", rest_apis.pdf, name="pdfRestPk"),
    path("rest/part/", rest_apis.part, name="partRest"),
    path("rest/part/<int:pk>", rest_apis.part, name="partRestPk"),
]
