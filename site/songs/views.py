from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Song


class SongList(ListView):
    """View for viewing all songs."""

    model = Song


class SongDetail(DetailView):
    """View for viewing a single song."""

    model = Song
