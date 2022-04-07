"""Views for the 'dashboard'-module."""
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic import RedirectView, TemplateView

from comments.models import Comment
from common.utils import random_sample_queryset
from events.models import Event
from minutes.models import Minutes
from pictures.models import Gallery, Image
from quotes.models import Quote


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
        return random_sample_queryset(Quote.objects.all(), 2)

    def get_events(self):
        """Returns all upcoming events the next month, or up to 5 later events."""
        upcoming_next_month = Event.objects.upcoming().filter(
            start_time__lte=timezone.now() + timedelta(days=31),
        )
        if upcoming_next_month.count() >= 5:
            return upcoming_next_month

        return Event.objects.upcoming()[:5]

    def get_minutes(self):
        """Returns the 5 most recent minutes."""
        return Minutes.objects.all()[:5]

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

    def get_context_data(self, **kwargs):
        kwargs["latest_quotes"] = self.get_latest_quotes()
        kwargs["random_quotes"] = self.get_random_quotes()
        kwargs["events"] = self.get_events()
        kwargs["minutes"] = self.get_minutes()
        kwargs["latest_galleries"] = self.get_latest_galleries()
        kwargs["random_images"] = self.get_random_images()
        kwargs["latest_comments"] = self.get_latest_comments()
        return super().get_context_data(**kwargs)
