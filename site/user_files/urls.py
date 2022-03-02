from django.urls import path

from . import views

app_name = "user_files"

urlpatterns = [
    path("", views.FileList.as_view(), name="FileList"),
]
