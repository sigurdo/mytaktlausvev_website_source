from django.contrib import admin
from .models import Gallery, Image


class ImageInline(admin.TabularInline):
    model = Image


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ImageInline,)


class ImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "gallery")
    search_fields = ("image", "gallery__title")


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
