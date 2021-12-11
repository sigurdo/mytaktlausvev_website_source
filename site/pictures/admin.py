from django.contrib import admin
from .models import Gallery


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Gallery, GalleryAdmin)
