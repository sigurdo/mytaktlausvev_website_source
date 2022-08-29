from django.contrib import admin

from .models import Event, EventAttendance, EventCategory


class EventAttendanceInline(admin.TabularInline):
    model = EventAttendance


class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_time")
    list_filter = ("category",)
    list_editable = ("category",)
    search_fields = ("title",)

    prepopulated_fields = {"slug": ("title",)}
    inlines = (EventAttendanceInline,)


class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ("event", "person", "status")
    search_fields = ("event__title", "person__name")


admin.site.register(Event, EventAdmin)
admin.site.register(EventAttendance, EventAttendanceAdmin)
admin.site.register(EventCategory)
