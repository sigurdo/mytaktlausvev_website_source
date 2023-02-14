from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom, InlineFormsetUpdateView
from common.mixins import PermissionOrCreatedMixin

from .forms import GalleryForm, ImageCreateForm, ImageFormSet
from .models import Gallery, Image


def nav_tabs_gallery_edit(gallery):
    """Returns tab data for editing a gallery."""
    return [
        {
            "url": reverse("pictures:GalleryUpdate", args=[gallery.slug]),
            "name": "Rediger galleri",
        },
        {
            "url": reverse("pictures:ImageCreate", args=[gallery.slug]),
            "name": "Last opp bilete",
        },
    ]


class GalleryList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    """View for viewing all galleries."""

    model = Gallery
    context_object_name = "galleries"
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("images", "events")
            .exclude(images__isnull=True)
            .order_by("-date")
        )

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("pictures:GalleryList"), "Fotoarkiv")


class NewestImagesList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Image
    context_object_name = "images"
    paginate_by = 50
    breadcrumb_parent = GalleryList

    def get_queryset(self):
        return super().get_queryset().select_related("gallery").order_by("-uploaded")


class GalleryDetail(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    """View for viewing a single gallery."""

    model = Image
    context_object_name = "images"
    paginate_by = 50
    template_name = "pictures/gallery_detail.html"
    breadcrumb_parent = GalleryList

    gallery = None

    def get_gallery(self):
        if not self.gallery:
            self.gallery = get_object_or_404(Gallery, slug=self.kwargs["slug"])
        return self.gallery

    def get_queryset(self):
        return super().get_queryset().filter(gallery=self.get_gallery())

    def get_context_data(self, **kwargs):
        kwargs["gallery"] = self.get_gallery()
        return super().get_context_data(**kwargs)

    @classmethod
    def get_breadcrumb(cls, gallery, **kwargs):
        return Breadcrumb(gallery.get_absolute_url(), gallery)


class GalleryCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    """View for creating a gallery."""

    model = Gallery
    form_class = GalleryForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = GalleryList

    def get_success_url(self) -> str:
        return reverse("pictures:ImageCreate", args=[self.object.slug])


class ImageCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Image
    form_class = ImageCreateForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = GalleryDetail

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
        kwargs["form_title"] = f'Last opp bilete til "{self.get_gallery()}"'
        kwargs["nav_tabs"] = nav_tabs_gallery_edit(self.get_gallery())
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.get_gallery().save()
            return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("pictures:GalleryUpdate", args=[self.get_gallery().slug])

    def get_breadcrumbs_kwargs(self):
        return {"gallery": self.get_gallery()}


class GalleryUpdate(LoginRequiredMixin, BreadcrumbsMixin, InlineFormsetUpdateView):
    """View for updating a gallery and its images."""

    model = Gallery
    form_class = GalleryForm
    formset_class = ImageFormSet
    template_name_suffix = "_form_update"
    breadcrumb_parent = GalleryDetail

    def get_context_data(self, **kwargs):
        kwargs["nav_tabs"] = nav_tabs_gallery_edit(self.object)
        return super().get_context_data(**kwargs)

    def get_breadcrumbs_kwargs(self):
        return {"gallery": self.object}


class GalleryDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Gallery
    success_url = reverse_lazy("pictures:GalleryList")
    permission_required = ("pictures.delete_gallery", "pictures.delete_image")
    breadcrumb_parent = GalleryDetail

    def get_breadcrumbs_kwargs(self):
        return {"gallery": self.object}
