from django.urls import path

from . import views

urlpatterns = [
    path("", views.JulekalenderList.as_view(), name="julekalender_list"),
    path("ny", views.JulekalenderCreate.as_view(), name="julekalender_create"),
    path("<int:pk>", views.JulekalenderDetail.as_view(), name="julekalender_detail"),
    path("nytt", views.WindowCreate.as_view(), name="window_create"),
]
