from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Minutes


class MinutesList(LoginRequiredMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50


class MinutesDetail(LoginRequiredMixin, DetailView):
    model = Minutes
