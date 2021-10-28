from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("ny/", views.EventCreate.as_view(), name="new"),
    path("<slug:slug>/", views.EventDetail.as_view(), name="detail"),
    # path("rediger/<int:event_id>", views.update_event, name="update_event"),
    # path("vis/<int:event_id>/", views.event_details, name="details"),
    # path(
    #     "deltek/<int:event_id>/<int:attendance_status>",
    #     views.declare_attendance,
    #     name="attend",
    # ),
]
