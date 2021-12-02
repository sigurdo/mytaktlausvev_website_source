"""Admin settings for the 'sheetmusic'-app"""

from django.contrib.admin import site, ModelAdmin
from .models import Score, Pdf, Part


class ScoreAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PartAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


site.register(Score, ScoreAdmin)
site.register(Pdf)
site.register(Part, PartAdmin)
