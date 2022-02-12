"""Views for quotes-app"""
from django.urls import reverse
import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http.response import Http404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from quotes.models import Quote

from .forms import QuoteForm


class QuoteNew(LoginRequiredMixin, CreateView):
    """View-function for new-quote-form"""
    model = Quote 
    form_class = QuoteForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("quotes:quotes")    


class QuoteList(LoginRequiredMixin, ListView):
    """View-function for displaying all quotes"""
    model = Quote
    context_object_name = "quotes"
    paginate_by = 50

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(public=True)


class QuoteUpdate(PermissionRequiredMixin, UpdateView):
    """View-function for editing quotes"""

    model = Quote
    form_class = QuoteForm
    template_name = "common/form.html"
    permission_required = "quotes.change_quote"

    def get_context_data(self, **kwargs):
        #kwargs["breadcrumbs"] = self.object.breadcrumbs(include_self=True)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("quotes:quotes")
