from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CASCADE, ForeignKey, IntegerField, Model, UniqueConstraint
from django.urls import reverse

from common.models import ArticleMixin


class AdventCalendar(Model):
    """Model representing a year's advent calendar."""

    year = IntegerField("år", primary_key=True)

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

    advent_calendar = ForeignKey(
        AdventCalendar,
        on_delete=CASCADE,
        related_name="windows",
        verbose_name="kalender",
    )
    index = IntegerField(
        "index",
        validators=[MinValueValidator(1), MaxValueValidator(24)],
    )

    def __str__(self):
        return f"Julekalender {self.advent_calendar.year}, luke {self.index}"

    def get_absolute_url(self):
        return reverse(
            "advent_calendar:AdventCalendarDetail", args=[self.advent_calendar.year]
        )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["advent_calendar", "index"], name="uniqueWindow")
        ]
        verbose_name = "luke"
        verbose_name_plural = "luker"
