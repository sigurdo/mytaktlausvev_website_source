from django.contrib import admin

from .models import Comment


class CommentAdminCustom(admin.ModelAdmin):
    list_display = ("__str__", "created_by", "created")
    search_fields = ("comment",)


admin.site.register(Comment, CommentAdminCustom)
