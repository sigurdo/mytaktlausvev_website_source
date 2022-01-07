import pgtrigger
from autoslug import AutoSlugField
from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    Model,
    TextChoices,
)
from django.db.models.constraints import UniqueConstraint
from django.urls.base import reverse

from common.models import ArticleMixin


class PollType(TextChoices):
    SINGLE_CHOICE = "SINGLE_CHOICE", "Eitt val"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE", "Fleirval"


# Restricts changing a poll's type since that would invalidate votes.
@pgtrigger.register(
    pgtrigger.Protect(
        name="protect_poll_type_update",
        operation=pgtrigger.Update,
        condition=pgtrigger.Q(old__type__df=pgtrigger.F("new__type")),
    )
)
class Poll(ArticleMixin):
    title = None
    content = None
    question = CharField("spørsmål", max_length=255)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="question",
        unique=True,
        editable=True,
    )
    public = BooleanField(
        "offentleg",
        help_text="Om avstemminga er open for ålmente.",
        default=False,
    )
    type = CharField(
        "type",
        max_length=255,
        choices=PollType.choices,
        default=PollType.SINGLE_CHOICE,
    )

    def get_absolute_url(self):
        return reverse("polls:PollRedirect", args=[self.slug])

    def __str__(self):
        return self.question

    def votes(self):
        """Returns the votes for this poll."""
        return Vote.objects.filter(choice__poll=self)

    def num_votes(self):
        """Returns the total amount of votes for this poll."""
        return self.votes().count()

    def num_voting(self):
        """Returns the amount of people who have voted for this people."""
        return self.votes().distinct("user").count()

    def has_voted(self, user):
        """Returns whether or not `user` has voted for this poll."""
        return self.votes().filter(user=user).exists()

    class Meta:
        ordering = ["-submitted"]
        get_latest_by = "submitted"
        verbose_name = "avstemming"
        verbose_name_plural = "avstemmingar"


class Choice(Model):
    text = CharField("val", max_length=255)
    poll = ForeignKey(
        Poll,
        on_delete=CASCADE,
        related_name="choices",
        verbose_name="avstemming",
    )
    order = FloatField(
        "rekkjefølgje",
        default=0,
        help_text="Definerer rekkjefølgja til val. Val med lik rekkjefølgje blir sortert etter namn.",
    )

    def __str__(self):
        return self.text

    def percentage(self):
        """
        Returns the number of votes for this choice
        as a percentage of the poll's total amount of votes.
        """
        num_votes = self.poll.num_votes()
        if num_votes:
            ratio = self.votes.count() / num_votes
        else:
            ratio = 0
        return f"{ratio:.0%}"

    class Meta:
        verbose_name = "val"
        verbose_name_plural = "val"
        ordering = ["order", "text"]


class Vote(Model):
    choice = ForeignKey(
        Choice,
        on_delete=CASCADE,
        related_name="votes",
        verbose_name="val",
    )
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="poll_votes",
        verbose_name="brukar",
    )
    created = DateTimeField("lagt ut", auto_now_add=True)

    def __str__(self):
        return f"{self.choice} - {self.choice.poll} {self.user}"

    class Meta:
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"
        constraints = [
            UniqueConstraint(
                name="one_vote_per_user_per_choice", fields=["choice", "user"]
            )
        ]
