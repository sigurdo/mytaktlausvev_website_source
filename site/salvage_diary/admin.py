"""Admin settings for the 'salvageDiary'-app"""

from django.contrib import admin

from .models import Mascot, SalvageDiaryEntryExternal, SalvageDiaryEntryInternal


class MascotAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "password",
        "get_creators",
    )
    filter_horizontal = ("creators",)

    readonly_fields = ("created", "created_by", "modified", "modified_by")

    @admin.display(description="skapere")
    def get_creators(self, obj):
        return obj.get_creators()


class SalvageDiaryAdminExternal(admin.ModelAdmin):
    list_display = ("title", "mascot", "thieves")


class SalvageDiaryAdminInternal(admin.ModelAdmin):
    list_display = ("title", "item", "thieves", "get_involved_users")
    filter_horizontal = ("users",)

    readonly_fields = ("created", "created_by", "modified", "modified_by")

    @admin.display(description="involverte medlemmar")
    def get_involved_users(self, obj):
        return obj.get_users()


admin.site.register(Mascot, MascotAdmin)
admin.site.register(SalvageDiaryEntryExternal, SalvageDiaryAdminExternal)
admin.site.register(SalvageDiaryEntryInternal, SalvageDiaryAdminInternal)
