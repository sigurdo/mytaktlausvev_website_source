"""Urls for the 'sheetmusic'-app"""
from django.urls import path
from sheetmusic import views
from sheetmusic import rest_apis

urlpatterns = [
    path("", views.sheetmusic, name="sheetmusic"),
    path("score/create/", views.createScore, name="createScore"),
    path("score/delete/<int:score_id>", views.deleteScore, name="deleteScore"),
    path("pdf/upload/<int:score_id>/", views.uploadPdf, name="uploadPdf"),
    path("rest/score", rest_apis.score, name="scoreRest"),
    path("rest/score/<int:score_id>", rest_apis.score, name="scoreRestId"),
]
