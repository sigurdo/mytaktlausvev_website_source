from django.urls import path

from . import views

urlpatterns = [
    path("", views.julekalenders, name="julekalenders"),
    path("<int:year>", views.julekalender, name="calendar"),
]
