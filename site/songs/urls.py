from django.urls import path
from . import views

urlpatterns = [
    path("", views.SongList.as_view(), name="song_list"),
    path("ny", views.SongCreate.as_view(), name="song_create"),
    path("<slug:slug>", views.SongDetail.as_view(), name="song_detail"),
    path("<slug:slug>/rediger", views.SongUpdate.as_view(), name="song_update"),
]
