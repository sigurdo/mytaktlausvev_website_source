from django.urls import path

from . import views

app_name = "advent_calendar"

urlpatterns = [
    path("", views.AdventCalendarList.as_view(), name="AdventCalendarList"),
    path("ny/", views.AdventCalendarCreate.as_view(), name="AdventCalendarCreate"),
    path(
        "<int:pk>/", views.AdventCalendarDetail.as_view(), name="AdventCalendarDetail"
    ),
    path("<int:year>/ny/", views.WindowCreate.as_view(), name="WindowCreate"),
    path(
        "<int:year>/<int:index>/rediger/",
        views.WindowUpdate.as_view(),
        name="WindowUpdate",
    ),
    path(
        "<int:year>/<int:index>/slett/",
        views.WindowDelete.as_view(),
        name="WindowDelete",
    ),
]
