from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from minutes.forms import MinutesForm

from .models import Minutes


class MinutesList(LoginRequiredMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50


class MinutesDetail(LoginRequiredMixin, DetailView):
    model = Minutes


class MinutesCreate(LoginRequiredMixin, CreateView):
    model = Minutes
    form_class = MinutesForm
    template_name = "common/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
