from django.urls import path

from . import views

app_name = "pictures"

urlpatterns = [
    path("", views.GalleryList.as_view(), name="GalleryList"),
    path("nytt-galleri/", views.GalleryCreate.as_view(), name="GalleryCreate"),
    path("<slug:slug>/", views.GalleryDetail.as_view(), name="GalleryDetail"),
    path("<slug:slug>/nye-bilete/", views.ImageCreate.as_view(), name="ImageCreate"),
    path("<slug:slug>/rediger/", views.GalleryUpdate.as_view(), name="GalleryUpdate"),
]
