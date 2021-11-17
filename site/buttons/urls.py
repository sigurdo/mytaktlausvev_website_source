from django.urls import path
from . import views

app_name = "buttons"

urlpatterns = [
    path("", views.Buttons.as_view(), name="buttons"),
    path("skiltmerke.pdf", views.Buttons.as_view(), name="buttons_with_filename"),
]
