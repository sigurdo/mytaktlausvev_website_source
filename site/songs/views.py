from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Song
from .forms import SongForm


class SongList(ListView):
    """View for viewing all songs."""

    model = Song


class SongDetail(DetailView):
    """View for viewing a single song."""

    model = Song


class SongCreate(LoginRequiredMixin, CreateView):
    """View for creating a song."""

    model = Song
    form_class = SongForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SongUpdate(LoginRequiredMixin, UpdateView):
    """View for updating a song."""

    model = Song
    form_class = SongForm
    template_name = "common/form.html"
