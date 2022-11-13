"""Admin settings for the 'quotes'-app"""

from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "quoted_as_or_users_view", "get_involved_users", "created")
    search_fields = ("quote", "quoted_as")
    filter_horizontal = ("users",)

    @admin.display(description="Sitert som")
    def quoted_as_or_users_view(self, obj):
        return obj.quoted_as_or_users()

    @admin.display(description="involverte brukarar")
    def get_involved_users(self, obj):
        return ", ".join(user.get_name() for user in obj.users.all())


admin.site.register(Quote, QuoteAdmin)
