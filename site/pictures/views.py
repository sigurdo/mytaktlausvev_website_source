from django.views.generic import DetailView, CreateView, UpdateView
from .models import Gallery
from .forms import GalleryForm


class GalleryDetail(DetailView):
    """View for viewing a single gallery."""

    model = Gallery


class GalleryCreate(CreateView):
    """View for creating an gallery."""

    model = Gallery
    form_class = GalleryForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class GalleryUpdate(UpdateView):
    """View for updating a gallery."""

    model = Gallery
    form_class = GalleryForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
