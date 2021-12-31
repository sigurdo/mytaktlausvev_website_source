from django.contrib.admin import site, ModelAdmin
from .models import NavbarItem

class NavbarItemAdmin(ModelAdmin):
    list_display = ("text", "link", "order", "type", "parent")
    ordering = ["order", "text"]

site.register(NavbarItem, NavbarItemAdmin)
