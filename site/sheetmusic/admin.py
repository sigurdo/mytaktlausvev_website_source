"""Admin settings for the 'sheetmusic'-app"""

from django.contrib.admin import ModelAdmin, site

from .models import Part, Pdf, Score


class ScoreAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PartAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


site.register(Score, ScoreAdmin)
site.register(Pdf)
site.register(Part, PartAdmin)
