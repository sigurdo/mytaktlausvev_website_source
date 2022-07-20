from django.urls import path

from . import views

app_name = "buttons"

urlpatterns = [
    path("", views.ButtonsView.as_view(), name="ButtonsView"),
    path("nytt-design/", views.ButtonDesignCreate.as_view(), name="ButtonDesignCreate"),
]
