from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "parent",
        "public",
        "comments_allowed",
        "created_by",
        "created",
    )
    search_fields = ("title", "parent__title", "created_by__name")
    list_filter = ("public", "comments_allowed")
    readonly_fields = ("created", "created_by", "modified", "modified_by")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
