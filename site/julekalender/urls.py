from django.urls import path

from . import views

urlpatterns = [
    path("", views.JulekalenderList.as_view(), name="julekalender_list"),
    path("ny", views.JulekalenderCreate.as_view(), name="julekalender_create"),
    path("<int:year>", views.julekalender, name="calendar"),
]
