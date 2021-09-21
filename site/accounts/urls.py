from django.urls import include, path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import ProfileDetail

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("profil/<slug:slug>/", ProfileDetail.as_view(), name="profile"),
    path("", include("django.contrib.auth.urls")),
]
