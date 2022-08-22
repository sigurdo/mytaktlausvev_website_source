from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


def repertoire_breadcrumbs(current=False, repertoire=None):
    breadcrumbs = [
        Breadcrumb(
            reverse("repertoire:RepertoireList"),
            "Alle repertoar",
        )
    ]
    if current:
        breadcrumbs.append(
            Breadcrumb(
                reverse("repertoire:ActiveRepertoires"),
                "Aktive",
            )
        )
    if repertoire is not None:
        breadcrumbs.append(
            Breadcrumb(
                reverse("repertoire:RepertoireDetail", args=[repertoire.slug]),
                str(repertoire),
            )
        )
    return breadcrumbs


class RepertoireList(LoginRequiredMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    ordering = ["-timestamp"]


class ActiveRepertoires(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    template_name = "repertoire/active_repertoires.html"

    def get_queryset(self):
        return Repertoire.objects.active()

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs()


class RepertoireDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Repertoire
    context_object_name = "repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(current=self.object.is_active())


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
        return repertoire_breadcrumbs(current=True)


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
        return repertoire_breadcrumbs(
            current=self.object.is_active(), repertoire=self.object
        )


class RepertoireDelete(PermissionRequiredMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Repertoire
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.delete_repertoire"

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(
            current=self.object.is_active(), repertoire=self.object
        )


class RepertoirePdf(LoginRequiredMixin, BreadcrumbsMixin, SingleObjectMixin, FormView):
    model = Repertoire
    template_name = "repertoire/repertoire_pdf.html"
    form_class = RepertoirePdfFormset

    def get_breadcrumbs(self):
        return repertoire_breadcrumbs(
            current=self.object.is_active(), repertoire=self.object
        )

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
