"""Views for quotes-app"""
<<<<<<< HEAD
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
from common.mixins import PermissionOrCreatedMixin
=======
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c

from quotes.models import Quote

from .forms import QuoteForm


class QuoteNew(LoginRequiredMixin, CreateView):
    """View-function for new-quote-form"""
<<<<<<< HEAD
    model = Quote 
=======

    model = Quote
>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c
    form_class = QuoteForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
<<<<<<< HEAD
        return reverse("quotes:quotes")    
=======
        return reverse("quotes:quotes")
>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c


class QuoteList(LoginRequiredMixin, ListView):
    """View-function for displaying all quotes"""
<<<<<<< HEAD
=======

>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c
    model = Quote
    context_object_name = "quotes"
    paginate_by = 50

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(public=True)


<<<<<<< HEAD
class QuoteUpdate(PermissionOrCreatedMixin, UpdateView):
=======
class QuoteUpdate(PermissionRequiredMixin, UpdateView):
>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c
    """View-function for editing quotes"""

    model = Quote
    form_class = QuoteForm
    template_name = "common/form.html"
    permission_required = "quotes.change_quote"

    def get_context_data(self, **kwargs):
<<<<<<< HEAD
        #kwargs["breadcrumbs"] = self.object.breadcrumbs(include_self=True)
=======
        # kwargs["breadcrumbs"] = self.object.breadcrumbs(include_self=True)
>>>>>>> 72e35c61e40e8e32fd040e993d4548631456882c
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("quotes:quotes")
