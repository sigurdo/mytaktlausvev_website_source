""" Views for sheetmusic """

# Official python packages
import os
import threading
import json
from typing import Any, Dict

# Django packages
import django
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import BaseModelForm, ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import (
    CreateView,
    FormView,
    ProcessFormView,
    UpdateView,
    DeleteView,
    FormMixin,
)

# Modules from this app
from .models import Score, Pdf, Part, FavoritePart
from .forms import (
    ScoreForm,
    UploadPdfForm,
    EditPartFormSet,
    EditPartFormSetHelper,
    EditPdfFormset,
    EditPdfFormsetHelper,
)


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
    template_name = "sheetmusic/score_edit.html"
    permission_required = "sheetmusic.change_score"

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ScoreDelete(PermissionRequiredMixin, DeleteView):
    model = Score
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("sheetmusic:ScoreList")
    permission_required = "sheetmusic.delete_score"


class PartsUpdate(
    PermissionRequiredMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = EditPartFormSet
    template_name = "sheetmusic/score_edit.html"
    permission_required = (
        "sheetmusic.add_part",
        "sheetmusic.change_part",
        "sheetmusic.delete_part",
    )

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def get_form_kwargs(self) -> Dict[str, Any]:
        # We have to override get_form_kwargs() to restrict the queryset of the formset to only
        # the parts that are related to the current score.
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = Part.objects.filter(pdf__score=self.get_object())
        return kwargs

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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Here we have to inject the formset helper
        kwargs["helper"] = EditPartFormSetHelper
        return super().get_context_data(**kwargs)


class PdfsUpdate(
    PermissionRequiredMixin,
    FormMixin,
    SingleObjectMixin,
    TemplateResponseMixin,
    ProcessFormView,
):
    model = Score
    form_class = EditPdfFormset
    template_name = "sheetmusic/score_edit.html"
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
        return super().get_context_data(**kwargs)


class PdfsUpload(PermissionRequiredMixin, FormView):
    form_class = UploadPdfForm
    template_name = "sheetmusic/score_edit.html"
    context_object_name = "score"
    permission_required = ("sheetmusic.add_pdf", "sheetmusic.add_part")

    def get_object(self):
        return get_object_or_404(Score, slug=self.kwargs["slug"])

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs[self.context_object_name] = self.get_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        files = self.request.FILES.getlist("files")
        for file in files:
            score = Score.objects.get(slug=self.kwargs["slug"])
            pdf = Pdf.objects.create(score=score, file=file)
            pdf.save()
            match form["part_prediction"].value():
                case "sheatless":
                    # plz_wait is a simple hack used only by the test framework so that the
                    # server does not return a response before the PDF is done processing
                    plz_wait = self.request.POST.get("plz_wait", False)
                    if plz_wait:
                        pdf.find_parts()
                    else:
                        processPdfsThread = threading.Thread(target=pdf.find_parts)
                        processPdfsThread.start()
                case "filename":
                    predicted_name = os.path.splitext(os.path.basename(file.name))[0]
                    Part(
                        name=predicted_name,
                        pdf=pdf,
                        from_page=1,
                        to_page=pdf.num_of_pages(),
                    ).save()
                case "none":
                    pass
                case _:
                    raise ValidationError(
                        "Ulovleg stemmegjettingstrategi: {}".format(
                            form["part_prediction"].value()
                        )
                    )
        return super().form_valid(form)


class ScoreCreate(PermissionRequiredMixin, CreateView):
    model = Score
    form_class = ScoreForm
    template_name = "common/form.html"
    permission_required = "sheetmusic.add_score"
    success_url = reverse_lazy("sheetmusic:ScoreList")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ScoreList(LoginRequiredMixin, ListView):
    model = Score
    context_object_name = "scores"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        for score in context["scores"]:
            relations = FavoritePart.objects.filter(
                part__pdf__score=score, user=self.request.user
            )
            if len(relations) > 0:
                score.favorite_part = relations[0].part
        return context


class PartRead(LoginRequiredMixin, DetailView):
    model = Part
    template_name = "sheetmusic/part_read.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        score_slug = self.kwargs["score_slug"]
        slug = self.kwargs[self.slug_url_kwarg]
        return queryset.get(**{self.slug_field: slug}, pdf__score__slug=score_slug)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["pageUrls"] = [
            "/media/sheetmusic/images/{}/page_{}.jpg".format(obj.pdf.pk, pageNum)
            for pageNum in range(obj.from_page, obj.to_page + 1)
        ]
        return context


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
        content = self.get_object().pdf_file()
        return HttpResponse(content=content, content_type=self.content_type)


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
