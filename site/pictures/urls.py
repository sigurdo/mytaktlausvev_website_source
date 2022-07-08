from django.urls import path

from . import views

app_name = "pictures"

urlpatterns = [
    path("", views.GalleryList.as_view(), name="GalleryList"),
    path("nyaste-bilete/", views.NewestImagesList.as_view(), name="NewestImagesList"),
    path("nytt-galleri/", views.GalleryCreate.as_view(), name="GalleryCreate"),
    path("<slug:slug>/", views.GalleryDetail.as_view(), name="GalleryDetail"),
    path("<slug:slug>/rediger/", views.GalleryUpdate.as_view(), name="GalleryUpdate"),
    path(
        "<slug:slug>/rediger/nye-bilete/",
        views.ImageCreate.as_view(),
        name="ImageCreate",
    ),
    path(
        "<slug:slug>/rediger/slett/",
        views.GalleryDelete.as_view(),
        name="GalleryDelete",
    ),
]
