from django.contrib import admin

from .models import ContactCategory


class ContactCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


admin.site.register(ContactCategory, ContactCategoryAdmin)
