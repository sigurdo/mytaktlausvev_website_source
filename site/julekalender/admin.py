from django.contrib import admin

from .models import Julekalender, Window


class WindowAdmin(admin.ModelAdmin):
    list_display = ("calendar", "index", "title", "created_by")
    search_fields = ("title", "calendar__year")
    ordering = ["calendar", "-index"]


admin.site.register(Julekalender)
admin.site.register(Window, WindowAdmin)
