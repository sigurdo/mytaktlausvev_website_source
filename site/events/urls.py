from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("ny/", views.EventCreate.as_view(), name="EventCreate"),
    path("<int:year>/<slug:slug>/", views.EventDetail.as_view(), name="EventDetail"),
    path(
        "<int:year>/<slug:slug>/rediger/",
        views.EventUpdate.as_view(),
        name="EventUpdate",
    ),
    path(
        "<int:year>/<slug:slug>/svar/",
        views.EventAttendanceList.as_view(),
        name="EventAttendanceList",
    ),
    path(
        "<int:year>/<slug:slug>/svar/ny/",
        views.EventAttendanceCreate.as_view(),
        name="EventAttendanceCreate",
    ),
    path(
        "<int:year>/<slug:slug_event>/svar/<slug:slug_person>/rediger/",
        views.EventAttendanceUpdate.as_view(),
        name="EventAttendanceUpdate",
    ),
    path(
        "<int:year>/<slug:slug_event>/svar/<slug:slug_person>/slett/",
        views.EventAttendanceDelete.as_view(),
        name="EventAttendanceDelete",
    ),
    path("taktlaushendingar.ics", views.EventFeed(), name="EventFeed"),
]
