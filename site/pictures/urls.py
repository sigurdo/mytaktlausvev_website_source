from django.urls import path
from . import views

app_name = "pictures"

urlpatterns = [
    path("<slug:slug>/", views.GalleryDetail.as_view(), name="GalleryDetail"),
]
