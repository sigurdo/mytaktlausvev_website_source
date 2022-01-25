""" Views for sheetmusic """

# Official python packages
import json
import os
import threading
from difflib import SequenceMatcher
from typing import Any, Dict

import django
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import BaseModelForm, ValidationError
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

from common.views import DeleteViewCustom
from instruments.models import InstrumentType

from .forms import (
    EditPdfFormset,
    EditPdfFormsetHelper,
    PartsUpdateAllFormset,
    PartsUpdateFormset,
    ScoreForm,
    UploadPdfForm,
)
from .models import FavoritePart, Part, Pdf, Score


def nav_tabs_score_edit(score):
    """Returns nav tabs for editing a score."""
    return [
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


class ScoreView(LoginRequiredMixin, DetailView):
    model = Score

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        pdfs = Pdf.objects.filter(score=self.get_object())
        parts = Part.objects.filter(pdf__in=pdfs)
        for part in parts:
            part.favorite = part.is_favorite_for(self.request.user)

        context = super().get_context_data(**kwargs)
        context["pdfs"] = pdfs
        context["parts"] = parts
        context["parts_favorite"] = list(filter(lambda part: part.favorite, parts))
        return context


class ScoreUpdate(PermissionRequiredMixin, UpdateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/form.html"
    permission_required = "sheetmusic.change_score"

    def get_context_data(self, **kwargs):
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ScoreDelete(PermissionRequiredMixin, DeleteViewCustom):
    model = Score
    success_url = reverse_lazy("sheetmusic:ScoreList")
    permission_required = "sheetmusic.delete_score"


class PartsUpdateIndex(PermissionRequiredMixin, ListView):
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

    def get_context_data(self, **kwargs):
        kwargs["score"] = self.score
        return super().get_context_data(**kwargs)

    def setup(self, request, *args, **kwargs):
        self.score = get_object_or_404(Score, slug=kwargs["slug"])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Pdf.objects.filter(score=self.score)


class PartsUpdate(
    PermissionRequiredMixin,
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

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger stemmer for {self.get_object()}"
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current pdf.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf=self.get_object()).order_by(
            "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def get_queryset(self):
        return Pdf.objects.filter(score__slug=self.kwargs["score_slug"])

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        for subform in form.forms:
            subform.instance.pdf = self.get_object()
        form.save()
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().get(*args, **kwargs)


class PartsUpdateAll(
    PermissionRequiredMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = PartsUpdateAllFormset
    template_name = "common/form.html"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_success_url(self) -> str:
        return reverse("sheetmusic:PartsUpdateIndex", args=[self.get_object().slug])

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf__score=self.get_object()).order_by(
            "pdf", "from_page", "to_page", "instrument_type", "part_number"
        )
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Rediger alle stemmer for {self.get_object()}"
        return super().get_context_data(**kwargs)

    def get_form(self, **kwargs) -> BaseModelForm:
        # Here we have to modify the queryset of each subform of the formset
        formset = super().get_form(**kwargs)
        for form in formset.forms:
            form.fields["pdf"].queryset = self.get_object().pdfs
        return formset

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().post(*args, **kwargs)

    def get(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().get(*args, **kwargs)


class PdfsUpdate(
    PermissionRequiredMixin,
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

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = self.get_object().pdfs.all()
        return kwargs

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        # We must set self.object here to be compatible with SingleObjectMixin
        self.object = self.get_object()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["helper"] = EditPdfFormsetHelper()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.object)
        return super().get_context_data(**kwargs)


def find_instrument_type_from_filename(filename):
    filename = filename.lower()
    sequence_matcher = SequenceMatcher()
    for instrument_type in InstrumentType.objects.all():
        sequence_matcher.set_seq1(instrument_type.name.lower())
        for i in range(max(1, len(filename) - len(instrument_type.name) + 1)):
            sequence_matcher.set_seq2(filename[i : i + len(instrument_type.name)])
            if sequence_matcher.ratio() > 0.8:
                return instrument_type
    return InstrumentType.objects.first()


class PdfsUpload(PermissionRequiredMixin, FormView):
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs[self.context_object_name] = self.get_score()
        kwargs["object"] = self.get_score()
        kwargs["nav_tabs"] = nav_tabs_score_edit(self.get_score())
        return super().get_context_data(**kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        for file in form.files.getlist("files"):
            score = Score.objects.get(slug=self.kwargs["slug"])
            pdf = Pdf.objects.create(
                score=score, file=file, filename_original=file.name
            )
            match form["part_prediction"].value():
                case "sheatless":
                    # plz_wait is a simple hack used only by the test framework so that the
                    # server does not return a response before the PDF is done processing
                    plz_wait = self.request.POST.get("plz_wait", False)
                    if plz_wait:
                        pdf.find_parts_with_sheatless()
                    else:
                        processPdfsThread = threading.Thread(
                            target=pdf.find_parts_with_sheatless
                        )
                        processPdfsThread.start()
                case "filename":
                    filename = os.path.splitext(os.path.basename(file.name))[0]
                    predicted_type = find_instrument_type_from_filename(filename)
                    pdf.create_part_auto_number(
                        instrument_type=predicted_type,
                        note="funne automatisk",
                        from_page=1,
                        to_page=pdf.num_of_pages(),
                    )
                case "none":
                    pass
                case _:
                    raise ValidationError(
                        "Ulovleg stemmefinningsstrategi: {}".format(
                            form["part_prediction"].value()
                        )
                    )
        return super().form_valid(form)


class ScoreCreate(PermissionRequiredMixin, CreateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/form.html"
    permission_required = "sheetmusic.add_score"

    def get_success_url(self):
        return reverse("sheetmusic:PdfsUpload", args=[self.object.slug])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
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
