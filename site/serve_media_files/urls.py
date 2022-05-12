from django.urls import path

from . import views

app_name = "serve_media_files"

urlpatterns = [
    path("<path:path>", views.ServeAllMediaFiles.as_view(), name="ServeAllMediaFiles"),
]
