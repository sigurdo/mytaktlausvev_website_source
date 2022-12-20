from django.urls import path

from . import views

app_name = "pdfs"

urlpatterns = [
    path("pdf-lesar/", views.PdfReadMinimalView.as_view(), name="PdfReadMinimalView"),
]
