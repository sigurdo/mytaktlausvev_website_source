from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Max
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView

from common.views import InlineFormsetUpdateView

from .forms import GalleryForm, ImageCreateForm, ImageFormSet
from .models import Gallery, Image


def breadcrumbs(gallery=None):
    """Returns breadcrumbs for the gallery views."""
    breadcrumbs = [{"url": reverse("pictures:GalleryList"), "name": "Fotoarkiv"}]
    if gallery:
        breadcrumbs.append({"url": gallery.get_absolute_url(), "name": gallery})
    return breadcrumbs


class GalleryList(LoginRequiredMixin, ListView):
    """View for viewing all galleries."""

    model = Gallery
    context_object_name = "galleries"
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(images__isnull=True)
            .alias(latest_upload=Max("images__uploaded"))
            .order_by("-latest_upload")
        )


class GalleryDetail(LoginRequiredMixin, ListView):
    """View for viewing a single gallery."""

    model = Image
    context_object_name = "images"
    paginate_by = 50
    template_name = "pictures/gallery_detail.html"

    gallery = None

    def get_gallery(self):
        if not self.gallery:
            self.gallery = get_object_or_404(Gallery, slug=self.kwargs["slug"])
        return self.gallery

    def get_queryset(self):
        return super().get_queryset().filter(gallery=self.get_gallery())

    def get_context_data(self, **kwargs):
        kwargs["gallery"] = self.get_gallery()
        kwargs["breadcrumbs"] = breadcrumbs()
        return super().get_context_data(**kwargs)


class GalleryCreate(LoginRequiredMixin, CreateView):
    """View for creating an gallery."""

    model = Gallery
    form_class = GalleryForm
    template_name = "common/form.html"

    def get_context_data(self, **kwargs):
        kwargs["breadcrumbs"] = breadcrumbs()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("pictures:ImageCreate", args=[self.object.slug])


class ImageCreate(LoginRequiredMixin, CreateView):
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
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["gallery"] = self.get_gallery()
        kwargs["breadcrumbs"] = breadcrumbs(self.get_gallery())
        kwargs["form_title"] = f"Last opp bilete til {self.get_gallery()}"
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        return reverse("pictures:GalleryUpdate", args=[self.get_gallery().slug])


class GalleryUpdate(LoginRequiredMixin, InlineFormsetUpdateView):
    """View for updating a gallery and its images."""

    model = Gallery
    form_class = GalleryForm
    formset_class = ImageFormSet
    template_name_suffix = "_form_update"

    def get_context_data(self, **kwargs):
        kwargs["breadcrumbs"] = breadcrumbs(self.object)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
