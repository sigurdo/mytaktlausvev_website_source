"""Admin settings for the 'salvageDiary'-app"""

from django.contrib import admin

from .models import Mascot, SalvageDiaryEntry


class MascotAdmin(admin.ModelAdmin):
    list_display = ("name",)

    readonly_fields = ("created", "created_by", "modified", "modified_by")


class SalvageDiaryAdmin(admin.ModelAdmin):
    list_display = ("title", "mascot", "thieves")


admin.site.register(Mascot, MascotAdmin)
admin.site.register(SalvageDiaryEntry, SalvageDiaryAdmin)
