from django.contrib import admin
from django.db.models import Max

from .models import Forum, Post, Topic


class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "submitted", "forum")
    search_fields = ("title", "created_by__username", "forum__title")
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    list_display = ("content_short", "created_by", "submitted", "topic")
    search_fields = ("content_short", "created_by__username", "topic__title")


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
