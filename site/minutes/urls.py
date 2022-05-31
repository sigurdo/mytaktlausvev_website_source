from django.urls import path

from . import views

app_name = "minutes"

urlpatterns = [
    path("", views.MinutesList.as_view(), name="MinutesList"),
    path("ny/", views.MinutesCreate.as_view(), name="MinutesCreate"),
    path("<slug:slug>/", views.MinutesDetail.as_view(), name="MinutesDetail"),
    path("<slug:slug>/rediger/", views.MinutesUpdate.as_view(), name="MinutesUpdate"),
    path("<slug:slug>/slett/", views.MinutesDelete.as_view(), name="MinutesDelete"),
]
