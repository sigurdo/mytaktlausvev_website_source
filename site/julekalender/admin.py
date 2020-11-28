from django.contrib import admin

from julekalender.models import Julekalender, Window


@admin.register(Julekalender)
class JulekalenderAdmin(admin.ModelAdmin):
    pass


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    ordering = ["calendar", "-index"]
