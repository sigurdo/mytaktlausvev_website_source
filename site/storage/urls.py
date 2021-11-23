from django.urls import path
from . import views



urlpatterns = [
    path("", views.StorageAccessView.as_view(), name="storage")
]
