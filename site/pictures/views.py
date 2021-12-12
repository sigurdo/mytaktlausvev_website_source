from django.views.generic import DetailView, CreateView, UpdateView
from common.views import FormAndFormsetUpdateView
from .models import Gallery
from .forms import GalleryForm, ImageFormSet, ImageFormsetHelper


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


class GalleryUpdate(FormAndFormsetUpdateView):
    """View for updating a gallery and its images."""

    model = Gallery
    form_class = GalleryForm
    formset_class = ImageFormSet
    formset_helper = ImageFormsetHelper

    def form_valid(self, form, formset):
        form.instance.modified_by = self.request.user
        return super().form_valid(form, formset)
