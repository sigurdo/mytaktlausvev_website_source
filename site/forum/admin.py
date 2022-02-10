from django.contrib import admin

from .models import Forum, Topic


class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created", "forum")
    search_fields = ("title", "created_by__username", "forum__title")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
