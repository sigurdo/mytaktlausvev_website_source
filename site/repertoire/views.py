from typing import Any, Dict

from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.http import HttpResponse, HttpRequest

from common.views import FormAndFormsetUpdateView

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
        return reverse("repertoire:RepertoireList")

class RepertoireUpdate(LoginRequiredMixin, FormAndFormsetUpdateView):
    model = models.Repertoire
    form_class = forms.RepertoireUpdateForm
    formset_class = forms.RepertoireEntryUpdateFormset
    formset_helper = forms.RepertoireEntryUpdateFormsetHelper
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        return reverse("repertoire:RepertoireUpdate", kwargs={ "pk": self.get_object().pk })

class RepertoireDelete(LoginRequiredMixin, DeleteView):
    model = models.Repertoire
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
