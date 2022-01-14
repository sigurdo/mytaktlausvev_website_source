from django.contrib.admin import ModelAdmin, TabularInline, site

from .models import Choice, Poll, Vote


class ChoiceInline(TabularInline):
    model = Choice
    extra = 3


class PollAdmin(ModelAdmin):
    list_display = ["question", "created"]
    search_fields = ["question"]
    prepopulated_fields = {"slug": ("question",)}
    inlines = [ChoiceInline]

    def get_readonly_fields(self, request, obj=None):
        """
        Make `type` read-only when editing a poll
        since changing it invalidates votes.
        """
        if obj:
            return ["type"]
        else:
            return []


class ChoiceAdmin(ModelAdmin):
    list_display = ["text", "poll"]
    search_fields = ["text", "poll__question"]


class VoteAdmin(ModelAdmin):
    list_display = ["choice", "poll", "user"]
    search_fields = ["choice__text", "choice__poll__question", "user__username"]

    def poll(self, vote):
        return vote.choice.poll


site.register(Poll, PollAdmin)
site.register(Choice, ChoiceAdmin)
site.register(Vote, VoteAdmin)
