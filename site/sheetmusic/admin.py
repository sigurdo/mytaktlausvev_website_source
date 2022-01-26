"""Admin settings for the 'sheetmusic'-app"""

from django.contrib.admin import ModelAdmin, site

from .models import Part, Pdf, Score


class ScoreAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


site.register(Score, ScoreAdmin)
site.register(Pdf)
site.register(Part)
