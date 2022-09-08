"""Admin settings for the 'repertoire'-app"""

from django.contrib.admin import ModelAdmin, TabularInline, site

from .models import Repertoire, RepertoireEntry


class RepertoireEntryInline(TabularInline):
    model = RepertoireEntry
    extra = 1


class RepertoireAdmin(ModelAdmin):
    list_display = ["name", "active_until", "order"]
    list_editable = ["order"]
    prepopulated_fields = {"slug": ["name"]}
    inlines = [RepertoireEntryInline]


site.register(Repertoire, RepertoireAdmin)
site.register(RepertoireEntry)
