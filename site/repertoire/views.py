from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F
from django.http import FileResponse
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import (
    DeleteViewCustom,
    InlineFormsetCreateView,
    InlineFormsetUpdateView,
)
from sheetmusic.models import Part

from .forms import RepertoireEntryFormset, RepertoireForm, RepertoirePdfFormset
from .models import Repertoire


def repertoire_breadcrumbs(repertoire=None, show_repertoire=False):
    breadcrumbs = [
        Breadcrumb(
            reverse("repertoire:ActiveRepertoires"),
            "Repertoar",
        )
    ]
    if repertoire is not None:
        if not repertoire.is_active():
            breadcrumbs.append(
                Breadcrumb(
                    reverse("repertoire:OldRepertoires"),
                    "Gamle",
                )
            )
        if show_repertoire:
            breadcrumbs.append(
                Breadcrumb(
                    reverse("repertoire:RepertoireDetail", args=[repertoire.slug]),
                    str(repertoire),
                )
            )
    return breadcrumbs


class OldRepertoires(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    template_name = "repertoire/old_repertoires.html"
    ordering = [F("active_until").desc(nulls_first=True)]

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs()


class ActiveRepertoires(LoginRequiredMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    template_name = "repertoire/active_repertoires.html"

    def get_queryset(self):
        return Repertoire.objects.active()


class RepertoireDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Repertoire
    context_object_name = "repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(repertoire=self.object)


class RepertoireCreate(
    PermissionRequiredMixin, BreadcrumbsMixin, InlineFormsetCreateView
):
    model = Repertoire
    form_class = RepertoireForm
    formset_class = RepertoireEntryFormset
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.add_repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class RepertoireUpdate(
    PermissionRequiredMixin, BreadcrumbsMixin, InlineFormsetUpdateView
):
    model = Repertoire
    form_class = RepertoireForm
    formset_class = RepertoireEntryFormset
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.change_repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(repertoire=self.object, show_repertoire=True)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class RepertoireDelete(PermissionRequiredMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Repertoire
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.delete_repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(repertoire=self.object, show_repertoire=True)


class RepertoirePdf(LoginRequiredMixin, BreadcrumbsMixin, SingleObjectMixin, FormView):
    model = Repertoire
    template_name = "repertoire/repertoire_pdf.html"
    form_class = RepertoirePdfFormset

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(repertoire=self.object, show_repertoire=True)

    def get_initial(self):
        return [
            {
                "score": entry.score,
                "part": entry.score.find_user_part(self.request.user),
            }
            for entry in self.object.entries.all()
        ]

    def get_form(self, **kwargs):
        """
        Here we have to modify the queryset of each subform of the formset.
        """
        formset = super().get_form(**kwargs)
        initial = self.get_initial()
        for i, form in enumerate(formset.forms):
            score = initial[i]["score"]
            form.fields["part"].queryset = Part.objects.filter(pdf__score=score)
        return formset

    def form_valid(self, form):
        output_stream = form.save()
        filename = slugify(f"{self.object} {self.request.user}") + ".pdf"
        return FileResponse(
            output_stream,
            content_type="application/pdf",
            filename=filename,
        )

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Generer PDF for {self.object}"
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
