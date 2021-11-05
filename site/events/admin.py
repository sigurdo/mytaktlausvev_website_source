from django.contrib import admin
from .models import Event, EventAttendance


class EventAttendanceInline(admin.TabularInline):
    model = EventAttendance


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (EventAttendanceInline,)


admin.site.register(Event, EventAdmin)
admin.site.register(EventAttendance)
