from django.urls import path

from . import views

urlpatterns = [
    path("", views.julekalender, name="julekalender"),
    path("new", views.newJulekalender, name="newJulekalender"),
]
