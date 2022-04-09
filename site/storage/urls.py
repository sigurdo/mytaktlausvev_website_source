from django.urls import path

from . import views

app_name = "storage"

urlpatterns = [
    path("", views.StorageAccess.as_view(), name="StorageAccess"),
    path("rediger/", views.StorageAccessUpdate.as_view(), name="StorageAccessUpdate"),
]
