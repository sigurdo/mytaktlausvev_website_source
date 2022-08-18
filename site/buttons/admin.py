from django.contrib import admin

from .models import ButtonDesign


class ButtonDesignAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by")
    search_fields = ("name", "created_by__get_name")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ButtonDesign, ButtonDesignAdmin)
