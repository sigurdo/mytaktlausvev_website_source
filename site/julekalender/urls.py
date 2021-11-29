from django.urls import path

from . import views

app_name = "advent_calendar"

urlpatterns = [
    path("", views.AdventCalendarList.as_view(), name="list"),
    path("ny/", views.AdventCalendarCreate.as_view(), name="create"),
    path("<int:pk>/", views.AdventCalendarDetail.as_view(), name="detail"),
    path("<int:year>/ny/", views.WindowCreate.as_view(), name="window_create"),
    path(
        "<int:year>/<int:index>/rediger/",
        views.WindowUpdate.as_view(),
        name="window_update",
    ),
]
