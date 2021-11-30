from django.urls import reverse
from django.db import models
from django.core import validators
from common.models import ArticleMixin


class AdventCalendar(models.Model):
    """Model representing a year's advent calendar."""

    year = models.IntegerField("år", primary_key=True)

    def __str__(self):
        return f"Julekalender {self.year}"

    def get_absolute_url(self):
        return reverse("advent_calendar:AdventCalendarDetail", args=[self.year])

    class Meta:
        ordering = ["-year"]
        verbose_name = "julekalender"
        verbose_name_plural = "julekalendrar"


class Window(ArticleMixin):
    """Model representing a window in an advent calendar."""

    advent_calendar = models.ForeignKey(
        AdventCalendar,
        on_delete=models.CASCADE,
        related_name="windows",
        verbose_name="kalender",
    )
    index = models.IntegerField(
        "index",
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(24)],
    )

    def __str__(self):
        return f"Julekalender {self.advent_calendar.year}, luke {self.index}"

    def get_absolute_url(self):
        return reverse(
            "advent_calendar:AdventCalendarDetail", args=[self.advent_calendar.year]
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["advent_calendar", "index"], name="uniqueWindow"
            )
        ]
        verbose_name = "luke"
        verbose_name_plural = "luker"
