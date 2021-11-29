from django.contrib import admin

from .models import AdventCalendar, Window


class WindowAdmin(admin.ModelAdmin):
    list_display = ("advent_calendar", "index", "title", "created_by")
    search_fields = ("title", "calendar__year")
    ordering = ["advent_calendar", "-index"]


admin.site.register(AdventCalendar)
admin.site.register(Window, WindowAdmin)
