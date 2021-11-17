from django.urls import path
from . import views

app_name = "buttons"

urlpatterns = [
    # There are 2 instances of this view so that the pdf is stored in the users
    # filesystem with the name skiltmerke.pdf instead of anything else the browser
    # might decide
    path("", views.Buttons.as_view(), name="buttons"),
    path("skiltmerke.pdf", views.Buttons.as_view(), name="buttons_with_filename"),
]
