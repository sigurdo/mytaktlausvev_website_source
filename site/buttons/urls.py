from django.urls import path
from . import views

app_name = "buttons"

urlpatterns = [
    # There are 2 instances of this view so that the pdf is stored in the users
    # filesystem with the name buttons.pdf instead of anything else the browser
    # might decide
    path("", views.ButtonsView.as_view(), name="ButtonsView"),
    path("buttons.pdf", views.ButtonsView.as_view(), name="ButtonsView_with_filename"),
]
