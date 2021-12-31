from django.contrib import admin

from .models import Choice, Poll, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    list_display = ["question", "submitted"]
    search_fields = ["question"]
    prepopulated_fields = {"slug": ("question",)}
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["text", "poll"]
    search_fields = ["text", "poll__question"]


class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user"]
    search_fields = ["choice__text", "choice__poll__question", "user__username"]

    def poll(self, vote):
        return vote.choice.poll


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
