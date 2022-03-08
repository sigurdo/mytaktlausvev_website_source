"""Views for quotes-app"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from common.mixins import PermissionOrCreatedMixin
from quotes.models import Quote

from .forms import QuoteForm

import random


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

    def get_template_names(self):
        random_number = random.randint(50,150)
        random_number2 = random.randint(1,random_number)
        random_number3 = random.randint(1, random_number)
        if (random_number2==random_number3):
            return "quotes/quote_list_shame.html"
        return super().get_template_names()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(public=True)


class QuoteUpdate(PermissionOrCreatedMixin, UpdateView):
    """View-function for editing quotes"""

    model = Quote
    form_class = QuoteForm
    template_name = "common/form.html"
    permission_required = "quotes.change_quote"

    def get_context_data(self, **kwargs):
        # kwargs["breadcrumbs"] = self.object.breadcrumbs(include_self=True)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("quotes:quotes")
