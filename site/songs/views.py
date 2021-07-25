from django.views.generic.list import ListView
from .models import Song


class SongList(ListView):
    """View for viewing all songs."""

    model = Song
