from django.contrib.admin import ModelAdmin, site

from .models import File


class FileAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


site.register(File, FileAdmin)
