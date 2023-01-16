from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.EventList.as_view(), name="EventList"),
    path("<int:year>/", views.EventList.as_view(), name="EventList"),
    path(
        "filter/<str:filter_type>/", views.EventList.as_view(), name="EventListFilter"
    ),
    path("ny/", views.EventCreate.as_view(), name="EventCreate"),
    path("<int:year>/<slug:slug>/", views.EventDetail.as_view(), name="EventDetail"),
    path(
        "<int:year>/<slug:slug>/rediger/",
        views.EventUpdate.as_view(),
        name="EventUpdate",
    ),
    path(
        "<int:year>/<slug:slug>/slett/",
        views.EventDelete.as_view(),
        name="EventDelete",
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
        "<int:year>/<slug:slug>/svar/ny/frå-oversikt/",
        views.EventAttendanceCreateFromList.as_view(),
        name="EventAttendanceCreateFromList",
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
    path(
        "(MYTAKTLAUSVEV_VARIABLE(appearance.events.feed.filename))",
        views.EventFeed(),
        name="EventFeed",
    ),
]
