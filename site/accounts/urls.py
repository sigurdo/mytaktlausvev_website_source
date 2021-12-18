from django.urls import path

from .views import ProfileDetail

app_name = "accounts"

urlpatterns = [
    path("profil/<slug:slug>/", ProfileDetail.as_view(), name="ProfileDetail"),
]
