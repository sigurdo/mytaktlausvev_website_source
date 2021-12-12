from django.views.generic import DetailView
from .models import Gallery


class GalleryDetail(DetailView):
    """View for viewing a single gallery."""

    model = Gallery
