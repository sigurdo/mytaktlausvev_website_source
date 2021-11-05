from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("ny/", views.EventCreate.as_view(), name="create"),
    path("<int:year>/<slug:slug>/", views.EventDetail.as_view(), name="detail"),
    path("<int:year>/<slug:slug>/rediger", views.EventUpdate.as_view(), name="update"),
    path(
        "<int:year>/<slug:slug>/registreringar",
        views.EventAttendanceList.as_view(),
        name="attendance_list",
    ),
    path(
        "<int:year>/<slug:slug>/registreringar/ny",
        views.EventAttendanceCreate.as_view(),
        name="attendance",
    ),
    # path("rediger/<int:event_id>", views.update_event, name="update_event"),
    # path("vis/<int:event_id>/", views.event_details, name="details"),
    # path(
    #     "deltek/<int:event_id>/<int:attendance_status>",
    #     views.declare_attendance,
    #     name="attend",
    # ),
]
