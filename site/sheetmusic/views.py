""" Views for sheetmusic """

# Official python packages
import json
from typing import Any, Dict

import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
    CreateView,
    FormMixin,
    FormView,
    ProcessFormView,
    UpdateView,
)

from common.mixins import BreadcrumbsMixin, PermissionOrCreatedMixin
from common.views import DeleteViewCustom

from .forms import (
    EditPdfFormset,
    EditPdfFormsetHelper,
    PartsUpdateAllFormset,
    PartsUpdateFormset,
    ScoreForm,
    UploadPdfForm,
)
from .models import FavoritePart, Part, Pdf, Score


def nav_tabs_score_edit(score, user):
    """Returns nav tabs for editing a score."""
    nav_tabs = [
        {
            "url": reverse("sheetmusic:ScoreUpdate", args=[score.slug]),
            "name": "Generelt",
            "permissions": ["sheetmusic.change_score"],
        },
        {
            "url": reverse("sheetmusic:PdfsUpdate", args=[score.slug]),
            "name": "PDFar",
            "permissions": ["sheetmusic.delete_pdf"],
        },
        {
            "url": reverse("sheetmusic:PdfsUpload", args=[score.slug]),
            "name": "PDF-opplasting",
            "permissions": ["sheetmusic.add_pdf", "sheetmusic.add_part"],
        },
    ]
    if score.created_by == user:
        for nav_tab in nav_tabs:
            nav_tab["permissions"] = []
    return nav_tabs


def sheetmusic_breadcrumbs(score=None, parts_update_index=False):
    breadcrumbs = [{"url": reverse("sheetmusic:ScoreList"), "name": "Alle notar"}]
    if score:
        breadcrumbs.append(
            {
                "url": reverse("sheetmusic:ScoreView", args=[score.slug]),
                "name": str(score),
            }
        )
    if parts_update_index:
        breadcrumbs.append(
            {
                "url": reverse("sheetmusic:PartsUpdateIndex", args=[score.slug]),
                "name": "Rediger stemmer",
            }
        )
    return breadcrumbs


class ScoreView(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Score

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user = self.request.user
        pdfs = Pdf.objects.filter(score=self.get_object())
        parts = Part.objects.filter(pdf__in=pdfs)
        for part in parts:
            part.favorite = part.is_favorite_for(user)
        context = super().get_context_data(**kwargs)
        context["pdfs"] = pdfs
        context["parts"] = parts
        context["parts_favorite"] = list(filter(lambda part: part.favorite, parts))
        if user.instrument_type:
            context["parts_instrument_group"] = list(
                filter(
                    lambda part: part.instrument_type.group
                    == user.instrument_type.group,
                    parts,
                )
            )
        return context


class ScoreCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/form.html"

    def get_success_url(self):
        return reverse("sheetmusic:PdfsUpload", args=[self.object.slug])

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ScoreUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/form.html"
    permission_required = "sheetmusic.change_score"

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.get_object())

    def get_context_data(self, **kwargs):
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object, self.request.user)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ScoreDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Score
    success_url = reverse_lazy("sheetmusic:ScoreList")
    permission_required = "sheetmusic.delete_score"

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.get_object())


class PartsUpdateIndex(PermissionOrCreatedMixin, BreadcrumbsMixin, ListView):
    model = Pdf
    context_object_name = "pdfs"
    template_name = "sheetmusic/parts_update_index.html"
    # This view does not really need to require any permissions since the actual
    # operations are protected by other views, but it is clean to have it since
    # the user won't find anything useful here at all if it does not have these
    # permsissions
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.score)

    def get_permission_check_object(self):
        return self.score

    def get_context_data(self, **kwargs):
        kwargs["score"] = self.score
        return super().get_context_data(**kwargs)

    def setup(self, request, *args, **kwargs):
        self.score = get_object_or_404(Score, slug=kwargs["slug"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Pdf.objects.filter(score=self.score)


class PartsUpdate(
    PermissionOrCreatedMixin,
    BreadcrumbsMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Pdf
    form_class = PartsUpdateFormset
    template_name = "sheetmusic/parts_update_form.html"
    context_object_name = "pdf"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_success_url(self) -> str:
        return reverse(
            "sheetmusic:PartsUpdateIndex", args=[self.get_object().score.slug]
        )

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(
            score=self.get_object().score, parts_update_index=True
        )

    def get_permission_check_object(self):
        return self.get_object().score

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger stemmer for {self.get_object()}"
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current pdf.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf=self.get_object()).order_by(
            "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def get_queryset(self):
        return Pdf.objects.filter(score__slug=self.kwargs["score_slug"])

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        for subform in form.forms:
            subform.instance.pdf = self.get_object()
        form.save()
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        """
        We must set self.object here to be compatible with SingleObjectMixin.
        """
        self.object = self.get_object()
        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        We must set self.object here to be compatible with SingleObjectMixin.
        """
        self.object = self.get_object()
        return super().get(*args, **kwargs)


class PartsUpdateAll(
    PermissionOrCreatedMixin,
    BreadcrumbsMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = PartsUpdateAllFormset
    template_name = "sheetmusic/parts_update_all_form.html"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.get_object().slug])

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.get_object(), parts_update_index=True)

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current score.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf__score=self.get_object()).order_by(
            "pdf", "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger alle stemmer for {self.get_object()}"
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs) -> BaseModelForm:
        """
        Here we have to modify the queryset of each subform of the formset.
        """
        formset = super().get_form(**kwargs)
        for form in formset.forms:
            form.fields["pdf"].queryset = self.get_object().pdfs
        return formset

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        form.save()
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        """
        We must set self.object here to be compatible with SingleObjectMixin.
        """
        self.object = self.get_object()
        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        We must set self.object here to be compatible with SingleObjectMixin.
        """
        self.object = self.get_object()
        return super().get(*args, **kwargs)


class PdfsUpdate(
    PermissionOrCreatedMixin,
    BreadcrumbsMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = EditPdfFormset
    template_name = "common/form.html"
    context_object_name = "score"
    permission_required = "sheetmusic.delete_pdf"

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.get_object())

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current score.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = self.get_object().pdfs.all()
        return kwargs

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        form.save()
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        """
        We must set self.object here to be compatible with SingleObjectMixin.
        """
        self.object = self.get_object()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["helper"] = EditPdfFormsetHelper()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object, self.request.user)
        return super().get_context_data(**kwargs)


class PdfsUpload(PermissionOrCreatedMixin, BreadcrumbsMixin, FormView):
    form_class = UploadPdfForm
    template_name = "common/form.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.add_pdf", "sheetmusic.add_part")

    score = None

    def get_score(self):
        if not self.score:
            self.score = get_object_or_404(Score, slug=self.kwargs["slug"])
        return self.score

    def get_success_url(self) -> str:
        return self.get_score().get_absolute_url()

    def get_breadcrumbs(self):
        return sheetmusic_breadcrumbs(score=self.get_score())

    def get_permission_check_object(self):
        return self.get_score()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs[self.context_object_name] = self.get_score()
        kwargs["object"] = self.get_score()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.get_score(), self.request.user)
        return super().get_context_data(**kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        score = Score.objects.get(slug=self.kwargs["slug"])
        form.save(score=score, plz_wait=self.request.POST.get("plz_wait", False))
        return super().form_valid(form)


class ScoreList(LoginRequiredMixin, ListView):
    model = Score
    context_object_name = "scores"


class PartPdf(LoginRequiredMixin, DetailView):
    model = Part
    content_type = "application/pdf"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        score_slug = self.kwargs["score_slug"]
        slug = self.kwargs[self.slug_url_kwarg]
        return queryset.get(**{self.slug_field: slug}, pdf__score__slug=score_slug)

    def render_to_response(self, _):
        pdf_stream = self.get_object().pdf_file()
        filename = self.get_object().pdf_filename()
        return FileResponse(
            pdf_stream, content_type=self.content_type, filename=filename
        )


class FavoritePartPdf(LoginRequiredMixin, DetailView):
    model = Score
    content_type = "application/pdf"

    def render_to_response(self, _):
        pdf_stream = self.get_object().favorite_parts_pdf_file(self.request.user)
        filename = self.get_object().favorite_parts_pdf_filename(self.request.user)
        return FileResponse(
            pdf_stream, content_type=self.content_type, filename=filename
        )


class FavoritePartUpdate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        part = Part.objects.get(pk=data["part_pk"])
        favorite = FavoritePart.objects.create(user=self.request.user, part=part)
        favorite.save()
        return django.http.JsonResponse(django.forms.models.model_to_dict(favorite))

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        favorite = FavoritePart.objects.get(user=request.user, part__pk=data["part_pk"])
        favorite.delete()
        return django.http.HttpResponse("deleted")
