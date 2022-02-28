"""Admin settings for the 'sheetmusic'-app"""

from django.contrib.admin import ModelAdmin, display, site

from .models import Part, Pdf, Score


class ScoreAdmin(ModelAdmin):
    list_display = ("title", "arrangement", "originally_from", "created")
    search_fields = ("title", "arrangement", "originally_from")
    prepopulated_fields = {"slug": ("title",)}


class PdfAdmin(ModelAdmin):
    list_display = ("filename_original", "score")
    search_fields = ("filename_original", "score__title")


class PartAdmin(ModelAdmin):
    list_display = ("__str__", "score_title")
    search_fields = ("instrument_type__name", "part_number", "note")

    @display(description="Note")
    def score_title(self, obj):
        return obj.pdf.score.title


site.register(Score, ScoreAdmin)
site.register(Pdf, PdfAdmin)
site.register(Part, PartAdmin)
