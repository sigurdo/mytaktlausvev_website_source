from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import FormView, ListView

from .forms import JacketsUpdateFormset
from .models import Jacket


class JacketList(LoginRequiredMixin, ListView):
    model = Jacket
    context_object_name = "jackets"




class JacketsUpdate(PermissionRequiredMixin, FormView):
    form_class = JacketsUpdateFormset
    template_name = "common/form.html"
    permission_required = (
        "uniforms.add_jacket",
        "uniforms.change_jacket",
        "uniforms.delete_jacket",
    )

    def get_success_url(self):
        return reverse("uniforms:JacketList")
    
    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger jakkeoversikt"
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        # We must explicitly save form since this a FormView and not an UpdateView
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)



