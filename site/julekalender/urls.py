from django.urls import path

from . import views

urlpatterns = [
    path("", views.julekalenders, name="julekalenders"),
    path("new", views.newJulekalender, name="newJulekalender"),
]
