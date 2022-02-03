from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Minutes


class MinutesList(LoginRequiredMixin, ListView):
    model = Minutes
    context_object_name = "minutes_list"
    paginate_by = 50
