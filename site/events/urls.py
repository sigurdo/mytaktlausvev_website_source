from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("ny/", views.EventCreate.as_view(), name="create"),
    path("<int:year>/<slug:slug>/", views.EventDetail.as_view(), name="detail"),
    path("<int:year>/<slug:slug>/rediger/", views.EventUpdate.as_view(), name="update"),
    path(
        "<int:year>/<slug:slug>/svar/",
        views.EventAttendanceList.as_view(),
        name="attendance_list",
    ),
    path(
        "<int:year>/<slug:slug>/svar/ny/",
        views.EventAttendanceCreate.as_view(),
        name="attendance_create",
    ),
    path(
        "<int:year>/<slug:slug_event>/svar/<slug:slug_person>/rediger/",
        views.EventAttendanceUpdate.as_view(),
        name="attendance_update",
    ),
    path(
        "<int:year>/<slug:slug_event>/svar/<slug:slug_person>/slett/",
        views.EventAttendanceDelete.as_view(),
        name="attendance_delete",
    ),
]