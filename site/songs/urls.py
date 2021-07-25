from django.urls import path
from . import views

urlpatterns = [
    path("", views.SongList.as_view(), name="song_list"),
]
