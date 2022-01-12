from django.urls import include, path

from .views import LoginViewCustom

urlpatterns = [
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("", include("django.contrib.auth.urls")),
]
