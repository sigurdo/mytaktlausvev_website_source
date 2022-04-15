from django import template

from polls.forms import MultiVoteForm, SingleVoteForm
from polls.models import Poll, PollType

register = template.Library()


@register.inclusion_tag("polls/includes/vote_or_results.html")
def vote_or_results(poll: Poll, user, next=None):
    form_class = (
        SingleVoteForm if poll.type == PollType.SINGLE_CHOICE else MultiVoteForm
    )
    form = form_class(poll, user, next)
    should_vote = user.is_authenticated and not poll.has_voted(user)

    return {"poll": poll, "form": form, "should_vote": should_vote}


@register.simple_tag
def votes_for_user(poll: Poll, user):
    """Returns the votes for a user on a poll."""
    return poll.votes().filter(user=user)
