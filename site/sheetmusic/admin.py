"""Admin settings for the 'sheetmusic'-app"""

from django.contrib.admin import ModelAdmin, TabularInline, display, site

from .models import EditFile, Part, Pdf, Score


class PdfInline(TabularInline):
    model = Pdf
    show_change_link = True


class EditFileInline(TabularInline):
    model = EditFile
    show_change_link = True


class ScoreAdmin(ModelAdmin):
    list_display = ("title", "arrangement", "originally_from", "created")
    search_fields = ("title", "arrangement", "originally_from")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (PdfInline, EditFileInline)


class PartInline(TabularInline):
    model = Part


class PdfAdmin(ModelAdmin):
    list_display = ("filename_original", "score")
    search_fields = ("filename_original", "score__title")
    inlines = (PartInline,)


class PartAdmin(ModelAdmin):
    list_display = ("__str__", "score")
    search_fields = (
        "instrument_type__name",
        "part_number",
        "note",
        "pdf__score__title",
    )

    @display(description="Note")
    def score(self, obj):
        return obj.pdf.score


class EditFileAdmin(ModelAdmin):
    list_display = ("filename_original", "score")
    search_fields = ("filename_original", "score__title")


site.register(Score, ScoreAdmin)
site.register(Pdf, PdfAdmin)
site.register(Part, PartAdmin)
site.register(EditFile, EditFileAdmin)
