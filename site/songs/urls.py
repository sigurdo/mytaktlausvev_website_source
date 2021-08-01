from django.urls import path
from . import views

urlpatterns = [
    path("", views.SongList.as_view(), name="song_list"),
    path("ny", views.SongCreate.as_view(), name="song_create"),
    path("<int:pk>", views.SongDetail.as_view(), name="song_detail"),
    path("<int:pk>/endre", views.SongUpdate.as_view(), name="song_update"),
]
