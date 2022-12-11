from django.urls import path

from . import views

app_name = "user_files"

urlpatterns = [
    path("", views.FileList.as_view(), name="FileList"),
    path("ny/", views.FileCreate.as_view(), name="FileCreate"),
    path("<slug:slug>/", views.FileRedirect.as_view(), name="FileRedirect"),
    path("<slug:slug>/rediger/", views.FileUpdate.as_view(), name="FileUpdate"),
    path("<slug:slug>/slett/", views.FileDelete.as_view(), name="FileDelete"),
]
