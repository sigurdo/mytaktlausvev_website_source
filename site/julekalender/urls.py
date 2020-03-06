from django.urls import path

from . import views

urlpatterns = [
    path("", views.julekalenders, name="julekalenders"),
    path("<int:year>", views.julekalender, name="julekalender"),
    path("<int:year>/<int:windowNumber>", views.window, name="julekalenderWindow"),
]
