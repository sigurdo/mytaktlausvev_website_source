"""Views for the 'dashboard'-module."""
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic import RedirectView, TemplateView

from accounts.models import UserCustom
from common.comments.models import Comment
from common.utils import comma_seperate_list, random_sample_queryset
from events.models import Event
from minutes.models import Minutes
from pictures.models import Gallery, Image
from quotes.models import Quote
from sheetmusic.models import Score


class DashboardRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse("dashboard:Dashboard")
        return reverse("articles:ArticleDetail", args=["om-oss"])


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_latest_quotes(self):
        """Returns the 2 latest quotes."""
        return Quote.objects.all()[0:2]

    def get_random_quotes(self):
        """Returns 2 random quotes."""
        quotes = Quote.objects.filter(
            created__lte=make_aware(datetime.now() - timedelta(days=1 * 365)),
            created__gte=make_aware(datetime.now() - timedelta(days=5 * 365)),
        )
        return random_sample_queryset(quotes, 2)

    def get_events(self):
        """Returns all upcoming events the next month, or up to 5 later events."""
        upcoming_next_month = Event.objects.upcoming().filter(
            start_time__lte=timezone.now() + timedelta(days=31),
        )
        if upcoming_next_month.count() >= 5:
            return upcoming_next_month

        return Event.objects.upcoming()[:5]

    def get_number_events_answered(self):
        """Returns the amount of upcoming events (within a year) a user has answered"""
        upcoming_events = Event.objects.upcoming().filter(
            start_time__lte=timezone.now() + timedelta(days=366),
        )
        upcoming_events_count = upcoming_events.count()
        events_answered = upcoming_events.filter(
            attendances__person=self.request.user
        ).count()

        if upcoming_events_count == events_answered:
            return upcoming_events_count
        return f"{events_answered}/{upcoming_events_count}"

    def get_minutes(self):
        """Returns the 5 most recently created minutes."""
        return Minutes.objects.order_by("-created")[:5]

    def get_latest_galleries(self):
        """Returns the 2 galleries with most recent image uploads."""
        return (
            Gallery.objects.all()
            .exclude(images__isnull=True)
            .alias(latest_upload=Max("images__uploaded"))
            .order_by("-latest_upload")[:2]
        )

    def get_random_images(self):
        """Returns 2 random images."""
        queryset = Image.objects.filter(
            uploaded__lte=make_aware(datetime.now() - timedelta(days=1 * 365)),
            uploaded__gte=make_aware(datetime.now() - timedelta(days=5 * 365)),
        )
        return random_sample_queryset(queryset, 2)

    def get_latest_comments(self):
        """Returns 5 most recent comments."""
        return Comment.objects.all().order_by("-created")[:5]

    def get_all_birthdays(self):
        return (
            UserCustom.objects.active()
            .exclude(birthdate=None)
            .order_by("birthdate__month", "birthdate__day")
        )

    def get_upcoming_birthdays(self):
        """Returns 5 most closely upcoming birthdays."""
        all_birthdays = self.get_all_birthdays()
        upcoming_in_year_filter = Q(birthdate__month__gt=timezone.now().month) | (
            Q(birthdate__month=timezone.now().month)
            & Q(birthdate__day__gte=timezone.now().day)
        )
        upcoming_birthdays = list(all_birthdays.filter(upcoming_in_year_filter)[:5])
        if len(upcoming_birthdays) < 5:
            upcoming_birthdays += list(
                all_birthdays.filter(~upcoming_in_year_filter)[
                    : (5 - len(upcoming_birthdays))
                ]
            )
        return upcoming_birthdays

    def get_current_birthdays(self):
        """Returns all current birthdays."""
        current_birthdays = self.get_all_birthdays().filter(
            birthdate__month=timezone.localdate().month,
            birthdate__day=timezone.localdate().day,
        )
        return comma_seperate_list([user.get_name() for user in current_birthdays])

    def get_birthday_song(self):
        """Returns birthday song score if it exists."""
        birthday_songs = Score.objects.filter(slug=settings.BIRTHDAY_SONG_SLUG)
        if birthday_songs.exists():
            birthday_song = birthday_songs.first()
            birthday_song.part = birthday_song.find_user_part(self.request.user)
            return birthday_song

    def get_latest_scores(self):
        """Returns 5 most recent scores."""
        return Score.objects.order_by("-created")[:5]

    def get_context_data(self, **kwargs):
        kwargs["latest_quotes"] = self.get_latest_quotes()
        kwargs["random_quotes"] = self.get_random_quotes()
        kwargs["events"] = self.get_events()
        kwargs["minutes"] = self.get_minutes()
        kwargs["latest_galleries"] = self.get_latest_galleries()
        kwargs["random_images"] = self.get_random_images()
        kwargs["latest_comments"] = self.get_latest_comments()
        kwargs["upcoming_birthdays"] = self.get_upcoming_birthdays()
        kwargs["current_birthdays"] = self.get_current_birthdays()
        if kwargs["current_birthdays"]:
            kwargs["birthday_song"] = self.get_birthday_song()
        kwargs["latest_scores"] = self.get_latest_scores()
        kwargs["number_events_answered"] = self.get_number_events_answered()
        return super().get_context_data(**kwargs)
