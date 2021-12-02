from django.urls import include, path
from django.contrib.auth.views import LoginView
from .forms import LoginForm

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="authentication/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("", include("django.contrib.auth.urls")),
]
