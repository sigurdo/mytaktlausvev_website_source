from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from common.views import InlineFormsetUpdateView

from .forms import GalleryForm, ImageCreateForm, ImageFormSet
from .models import Gallery, Image


class GalleryList(ListView):
    """View for viewing all galleries."""

    model = Gallery
    context_object_name = "galleries"

    def get_queryset(self):
        return super().get_queryset().exclude(images__isnull=True)


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

    def get_success_url(self) -> str:
        return reverse("pictures:ImageCreate", args=[self.object.slug])


class ImageCreate(CreateView):
    model = Image
    form_class = ImageCreateForm
    template_name = "common/form.html"

    gallery = None

    def get_gallery(self):
        if not self.gallery:
            self.gallery = get_object_or_404(Gallery, slug=self.kwargs["slug"])
        return self.gallery

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["gallery"] = self.get_gallery()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["gallery"] = self.get_gallery()
        kwargs["form_title"] = f"Last opp bilete til {self.get_gallery()}"
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        return reverse("pictures:GalleryUpdate", args=[self.get_gallery().slug])


class GalleryUpdate(InlineFormsetUpdateView):
    """View for updating a gallery and its images."""

    model = Gallery
    form_class = GalleryForm
    formset_class = ImageFormSet

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
