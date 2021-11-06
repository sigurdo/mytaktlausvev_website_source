from django.contrib import admin
from .models import Event, EventAttendance


class EventAttendanceInline(admin.TabularInline):
    model = EventAttendance


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (EventAttendanceInline,)
    list_display = ("title", "start_time")
    search_fields = ("title",)


class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ("event", "person", "status")
    search_fields = ("event__title", "person__name")


admin.site.register(Event, EventAdmin)
admin.site.register(EventAttendance, EventAttendanceAdmin)
