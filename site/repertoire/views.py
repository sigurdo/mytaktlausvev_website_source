from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F, Prefetch
from django.http import FileResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from sheetmusic.models import Part, Score

from .forms import RepertoireForm, RepertoirePdfFormset
from .models import Repertoire


class ActiveRepertoires(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    template_name = "repertoire/active_repertoires.html"

    def get_queryset(self):
        return Repertoire.objects.active(date=self.kwargs.get("date")).prefetch_related(
            Prefetch(
                "scores",
                queryset=Score.objects.annotate_user_has_favorite_parts(
                    self.request.user
                ),
            )
        )

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("repertoire:ActiveRepertoires"), "Repertoar")


class OldRepertoires(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Repertoire
    context_object_name = "repertoires"
    template_name = "repertoire/old_repertoires.html"
    ordering = [F("active_until").desc(nulls_first=True)]
    breadcrumb_parent = ActiveRepertoires

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(reverse("repertoire:OldRepertoires"), "Gamle")


class RepertoireDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    model = Repertoire
    context_object_name = "repertoire"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("created_by", "modified_by")
            .prefetch_related(
                Prefetch(
                    "scores",
                    queryset=Score.objects.annotate_user_has_favorite_parts(
                        self.request.user
                    ),
                )
            )
        )

    @classmethod
    def get_breadcrumb_parent(cls, repertoire, **kwargs):
        if repertoire.is_active():
            return ActiveRepertoires
        return OldRepertoires

    def get_breadcrumbs_kwargs(self):
        return {"repertoire": self.object}

    @classmethod
    def get_breadcrumb(cls, repertoire, **kwargs):
        return Breadcrumb(
            reverse("repertoire:RepertoireDetail", args=[repertoire.slug]),
            str(repertoire),
        )


class RepertoireCreate(PermissionRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Repertoire
    form_class = RepertoireForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.add_repertoire"
    breadcrumb_parent = ActiveRepertoires


class RepertoireUpdate(PermissionRequiredMixin, BreadcrumbsMixin, UpdateView):
    model = Repertoire
    form_class = RepertoireForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.change_repertoire"
    breadcrumb_parent = RepertoireDetail

    def get_breadcrumbs_kwargs(self):
        return {"repertoire": self.object}


class RepertoireDelete(PermissionRequiredMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Repertoire
    success_url = reverse_lazy("repertoire:ActiveRepertoires")
    permission_required = "repertoire.delete_repertoire"
    breadcrumb_parent = RepertoireDetail

    def get_breadcrumbs_kwargs(self):
        return {"repertoire": self.object}


class RepertoirePdf(LoginRequiredMixin, BreadcrumbsMixin, SingleObjectMixin, FormView):
    model = Repertoire
    template_name = "repertoire/repertoire_pdf.html"
    form_class = RepertoirePdfFormset
    breadcrumb_parent = RepertoireDetail

    def get_initial(self):
        return [
            {
                "score": score,
                "part": score.find_user_part(self.request.user),
            }
            for score in self.object.scores.all()
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
        return FileResponse(
            output_stream,
            content_type="application/pdf",
            filename=self.object.favorite_parts_pdf_filename(self.request.user),
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

    def get_breadcrumbs_kwargs(self):
        return {"repertoire": self.object}
