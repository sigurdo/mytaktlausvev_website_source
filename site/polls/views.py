from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from common.views import FormAndFormsetUpdateView

from .forms import ChoiceFormset, ChoiceFormsetHelper, PollForm
from .models import Poll


class PollUpdate(PermissionRequiredMixin, FormAndFormsetUpdateView):
    model = Poll
    form_class = PollForm
    formset_class = ChoiceFormset
    formset_helper = ChoiceFormsetHelper
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = (
        "polls.change_poll",
        "polls.add_choice",
        "polls.change_choice",
        "polls.delete_choice",
    )
