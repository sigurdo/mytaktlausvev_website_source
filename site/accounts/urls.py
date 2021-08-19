from django.urls import include, path
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("", include("django.contrib.auth.urls")),
]
