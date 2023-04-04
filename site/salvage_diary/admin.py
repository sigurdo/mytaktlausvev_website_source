"""Admin settings for the 'salvageDiary'-app"""

from django.contrib import admin

from .models import Mascot, SalvageDiaryEntryExternal, SalvageDiaryEntryInternal


class MascotAdmin(admin.ModelAdmin):
    list_display = ("name",)

    readonly_fields = ("created", "created_by", "modified", "modified_by")


class SalvageDiaryAdminExternal(admin.ModelAdmin):
    list_display = ("title", "mascot", "thieves")


class SalvageDiaryAdminInternal(admin.ModelAdmin):
    list_display = ("title", "item", "thieves")


admin.site.register(Mascot, MascotAdmin)
admin.site.register(SalvageDiaryEntryExternal, SalvageDiaryAdminExternal)
admin.site.register(SalvageDiaryEntryInternal, SalvageDiaryAdminInternal)
