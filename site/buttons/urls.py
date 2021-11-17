from django.urls import path
from . import views

app_name = "buttons"

urlpatterns = [
    path("", views.Buttons.as_view(), name="buttons"),
]
