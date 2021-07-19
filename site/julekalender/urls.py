from django.urls import path

from . import views

urlpatterns = [
    path("", views.julekalenders, name="calendar_list"),
    path("<int:year>", views.julekalender, name="calendar"),
]
