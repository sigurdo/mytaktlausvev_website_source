""" Views for sheetmusic """

import json
from typing import Any, Dict

import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin
from common.pdfs.views import PdfReadMinimalMixin

from .forms import (
    EditEditFileFormset,
    EditPdfFormset,
    EditPdfFormsetHelper,
    PartsUpdateAllFormset,
    PartsUpdateFormset,
    ScoreForm,
    UploadEditFilesForm,
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
        {
            "url": reverse("sheetmusic:EditFilesUpdate", args=[score.slug]),
            "name": "Redigeringsfiler",
            "permissions": ["sheetmusic.change_editfile", "sheetmusic.delete_editfile"],
        },
        {
            "url": reverse("sheetmusic:EditFilesUpload", args=[score.slug]),
            "name": "Redigeringsfilopplasting",
            "permissions": ["sheetmusic.add_editfile"],
        },
    ]
    if score.created_by == user:
        for nav_tab in nav_tabs:
            nav_tab["permissions"] = []
    return nav_tabs


class ScoreList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Score
    context_object_name = "scores"

    @classmethod
    def get_breadcrumb(cls, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=reverse("sheetmusic:ScoreList"),
            label="Alle notar",
        )

    def get_queryset(self):
        return Score.objects.annotate_user_has_favorite_parts(self.request.user)


class ScoreView(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Score
    breadcrumb_parent = ScoreList

    @classmethod
    def get_breadcrumb(cls, score, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=reverse("sheetmusic:ScoreView", args=[score.slug]),
            label=str(score),
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user = self.request.user
        parts = (
            Part.objects.annotate_is_favorite(user)
            .filter(pdf__in=self.object.pdfs.all())
            .select_related("pdf__score")
        )
        context = super().get_context_data(**kwargs)
        context["parts"] = parts
        context["parts_favorite"] = parts.filter(is_favorite=True)
        if user.instrument_type:
            context["parts_instrument_group"] = parts.filter(
                instrument_type__group=user.instrument_type.group
            )
        return context


class ScorePdf(LoginRequiredMixin, DetailView):
    model = Score
    content_type = "application/pdf"

    def render_to_response(self, _):
        pdf_stream, pdf_name = self.get_object().pdf_file()
        return FileResponse(
            pdf_stream, content_type=self.content_type, filename=pdf_name
        )


class ScoreZip(LoginRequiredMixin, DetailView):
    model = Score
    content_type = "application/zip"

    def render_to_response(self, _):
        zip_stream, zip_name = self.get_object().zip_file()
        return FileResponse(
            zip_stream, content_type=self.content_type, filename=zip_name
        )


class ScoreCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = ScoreList

    def get_success_url(self):
        return reverse("sheetmusic:PdfsUpload", args=[self.object.slug])


class ScoreUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/forms/form.html"
    permission_required = "sheetmusic.change_score"
    breadcrumb_parent = ScoreView

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.get_object(),
        }

    def get_context_data(self, **kwargs):
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object, self.request.user)
        return super().get_context_data(**kwargs)


class ScoreDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Score
    success_url = reverse_lazy("sheetmusic:ScoreList")
    permission_required = "sheetmusic.delete_score"
    breadcrumb_parent = ScoreView

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.get_object(),
        }


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
    breadcrumb_parent = ScoreView

    @classmethod
    def get_breadcrumb(cls, score, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=reverse("sheetmusic:PartsUpdateIndex", args=[score.slug]),
            label="Rediger stemmer",
        )

    def get_breadcrumbs_kwargs(self):
        return {"score": self.score}

    def get_permission_check_object(self):
        return self.score

    def get_context_data(self, **kwargs):
        kwargs["score"] = self.score
        kwargs["total_parts_count"] = Part.objects.filter(pdf__score=self.score).count()
        return super().get_context_data(**kwargs)

    def setup(self, request, *args, **kwargs):
        self.score = get_object_or_404(Score, slug=kwargs["slug"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Pdf.objects.filter(score=self.score).prefetch_related("parts")


class PartsUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SingleObjectMixin, FormView
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
    breadcrumb_parent = PartsUpdateIndex

    def get_breadcrumbs_kwargs(self):
        return {"score": self.object.score}

    def get_object(self, queryset=None):
        return get_object_or_404(
            Pdf, score__slug=self.kwargs["score_slug"], slug=self.kwargs["slug"]
        )

    def setup(self, request, *args, **kwargs):
        """Set `self.object` for `SingleObjectMixin` compatibility."""
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.object.score.slug])

    def get_permission_check_object(self):
        return self.object.score

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger stemmer for {self.object}"
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current pdf.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf=self.object).order_by(
            "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.object.score.save()

            for subform in form.forms:
                subform.instance.pdf = self.object
            form.save()
            return super().form_valid(form)


class PartsUpdateAll(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SingleObjectMixin, FormView
):
    model = Score
    form_class = PartsUpdateAllFormset
    template_name = "sheetmusic/parts_update_all_form.html"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )
    breadcrumb_parent = PartsUpdateIndex

    def get_breadcrumbs_kwargs(self):
        return {"score": self.object}

    def setup(self, request, *args, **kwargs):
        """Set `self.object` for `SingleObjectMixin` compatibility."""
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.object.slug])

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current score.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf__score=self.object).order_by(
            "pdf", "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger alle stemmer for {self.object}"
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs) -> BaseModelForm:
        """
        Here we have to modify the queryset of each subform of the formset.
        """
        formset = super().get_form(**kwargs)
        for form in formset.forms:
            form.fields["pdf"].queryset = self.object.pdfs
        return formset

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.object.save()

            form.save()
            return super().form_valid(form)


class PdfsUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SingleObjectMixin, FormView
):
    model = Score
    form_class = EditPdfFormset
    template_name = "common/forms/form.html"
    context_object_name = "score"
    permission_required = "sheetmusic.delete_pdf"
    breadcrumb_parent = ScoreView

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.get_object(),
        }

    def setup(self, request, *args, **kwargs):
        """Set `self.object` for `SingleObjectMixin` compatibility."""
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_form_kwargs(self) -> Dict[str, Any]:
        """
        We have to override get_form_kwargs() to restrict the queryset of the formset to only
        the parts that are related to the current score.
        """
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = self.object.pdfs.all()
        return kwargs

    def form_valid(self, form):
        """
        We must explicitly save the form because it is not done automatically by any ancestors.
        """
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.object.save()

            form.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["helper"] = EditPdfFormsetHelper()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object, self.request.user)
        return super().get_context_data(**kwargs)


class PdfsUpload(PermissionOrCreatedMixin, BreadcrumbsMixin, FormView):
    form_class = UploadPdfForm
    template_name = "common/forms/form.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.add_pdf", "sheetmusic.add_part")
    breadcrumb_parent = ScoreView

    score = None

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.get_score(),
        }

    def get_score(self):
        if not self.score:
            self.score = get_object_or_404(Score, slug=self.kwargs["slug"])
        return self.score

    def get_success_url(self) -> str:
        return self.get_score().get_absolute_url()

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


class PartDetail(LoginRequiredMixin, PdfReadMinimalMixin, DetailView):
    model = Part
    context_object_name = "part"

    def pdf_url(self):
        return self.get_object().get_pdf_url()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        score_slug = self.kwargs["score_slug"]
        slug = self.kwargs[self.slug_url_kwarg]
        return queryset.get(**{self.slug_field: slug}, pdf__score__slug=score_slug)


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


class EditFilesUpload(PermissionOrCreatedMixin, BreadcrumbsMixin, FormView):
    form_class = UploadEditFilesForm
    template_name = "common/forms/form.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.add_editfile",)
    breadcrumb_parent = ScoreView

    score = None

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.get_score(),
        }

    def get_score(self):
        if not self.score:
            self.score = get_object_or_404(Score, slug=self.kwargs["slug"])
        return self.score

    def get_success_url(self) -> str:
        return self.get_score().get_absolute_url()

    def get_permission_check_object(self):
        return self.get_score()

    def get_context_data(self, **kwargs):
        kwargs[self.context_object_name] = self.get_score()
        kwargs["object"] = self.get_score()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.get_score(), self.request.user)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.get_score().save()
            form.save(score=self.get_score())
            return super().form_valid(form)


class EditFilesUpdate(
    PermissionOrCreatedMixin, BreadcrumbsMixin, SingleObjectMixin, FormView
):
    model = Score
    form_class = EditEditFileFormset
    template_name = "common/forms/form.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.change_editfile", "sheetmusic.delete_editfile")
    breadcrumb_parent = ScoreView

    def get_breadcrumbs_kwargs(self):
        return {
            "score": self.object,
        }

    def setup(self, request, *args, **kwargs):
        """Set `self.object` for `SingleObjectMixin` compatibility."""
        super().setup(request, *args, **kwargs)
        self.object = self.get_object()

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = self.object.edit_files.all()
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            # Update `modified` and `modified_by`
            self.object.save()
            form.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object, self.request.user)
        return super().get_context_data(**kwargs)
