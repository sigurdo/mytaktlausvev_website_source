"""Admin settings for the 'repertoire'-app"""

from django.contrib.admin import ModelAdmin, site

from .models import Repertoire


class RepertoireAdmin(ModelAdmin):
    list_display = ["name", "active_until", "order"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ("created", "created_by", "modified", "modified_by")


site.register(Repertoire, RepertoireAdmin)
