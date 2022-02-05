from django.contrib.admin import ModelAdmin, site

from minutes.models import Minutes


class MinutesAdmin(ModelAdmin):
    list_display = ("title", "created_by", "date")
    search_fields = ("title", "created_by__username")

    prepopulated_fields = {"slug": ("title",)}


site.register(Minutes, MinutesAdmin)
