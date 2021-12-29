import pgtrigger
from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.db.models import constraints
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q

from common.models import ArticleMixin


class PollType(models.TextChoices):
    SINGLE_CHOICE = "SINGLE_CHOICE", "Einval"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE", "Fleirval"


class Poll(ArticleMixin):
    title = None
    content = None
    question = models.CharField("spørsmål", max_length=50)
    slug = AutoSlugField(
        verbose_name="lenkjenamn",
        populate_from="question",
        unique=True,
        editable=True,
    )
    public = models.BooleanField(
        "offentleg",
        help_text="Om avstemminga er open for ålmente.",
        default=False,
    )
    type = models.CharField(
        "type",
        max_length=255,
        choices=PollType.choices,
        default=PollType.SINGLE_CHOICE,
    )

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.question

    @property
    def num_votes(self):
        """Returns the total amount of votes for this poll."""
        return Vote.objects.filter(choice__poll=self).count()

    @property
    def num_voting(self):
        """Returns the amount of people who have voted for this people."""
        return Vote.objects.filter(choice__poll=self).distinct("user").count()

    class Meta:
        ordering = ["-submitted"]
        verbose_name = "avstemming"
        verbose_name_plural = "avstemmingar"


class Choice(models.Model):
    text = models.CharField("tekst", max_length=50)
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="avstemming",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "val"
        verbose_name_plural = "val"


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="votes",
        verbose_name="val",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="poll_votes",
        verbose_name="brukar",
    )

    def __str__(self):
        pass

    class Meta:
        verbose_name = "stemme"
        verbose_name_plural = "stemmer"
        constraints = [
            UniqueConstraint(
                name="one_vote_per_user_per_choice", fields=["choice", "user"]
            )
        ]
