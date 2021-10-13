from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.http import HttpResponse, HttpRequest

from . import models
import sheetmusic.models
from . import forms

# Create your views here.

class RepertoireList(ListView):
    model = models.Repertoire
    context_object_name = "repertoires"

class RepertoireCreate(LoginRequiredMixin, CreateView):
    model = models.Repertoire
    form_class = forms.RepertoireCreateForm
    template_name_suffix = "_create_form"

    def get_success_url(self) -> str:
        return reverse("repertoire")

class RepertoireUpdate(LoginRequiredMixin, UpdateView):
    model = models.Repertoire
    form_class = forms.RepertoireUpdateForm
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        return reverse("repertoire")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print("----------------------------------------------------------------------")
        print("| TODO:")
        print("| Entries:", self.get_object().entries)
        print("----------------------------------------------------------------------")
        return context

class RepertoireEntryCreate(LoginRequiredMixin, CreateView):
    model = models.RepertoireEntry
    form_class = forms.RepertoireEntryCreateForm
    template_name_suffix = "_create_form"

    def form_valid(self, form: forms.RepertoireEntryCreateForm) -> HttpResponse:
        form.instance.repertoire = models.Repertoire.objects.get(pk=self.kwargs['repertoire_pk'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("updateRepertoire", kwargs={ "pk": self.object.repertoire.pk })
