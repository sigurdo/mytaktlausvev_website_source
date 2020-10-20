from django.urls import path
from . import views

urlpatterns = [
    path("ny/", views.new_event, name="new_event"),
    path("rediger/<int:event_id>", views.update_event, name="update_event"),
    path("vis/<int:event_id>/", views.event_details, name="event_details"),
    path("deltek/<int:event_id>/<int:attendance_status>",
         views.declare_attendance, name="attend"),
]
