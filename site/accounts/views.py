from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView

from common.templatetags.markdown import markdown

from .forms import UserCustomCreateForm
from .models import UserCustom
from django.views.generic import ListView


class UserCustomCreate(PermissionRequiredMixin, CreateView):
    model = UserCustom
    form_class = UserCustomCreateForm
    template_name = "common/form.html"
    permission_required = "accounts.add_usercustom"

    def form_valid(self, form):
        response = super().form_valid(form)

        plain_text = render_to_string(
            "accounts/welcome_mail.md", {"username": self.object.username}
        )
        html = markdown(plain_text)
        send_mail(
            "Velkomen til Studentorchesteret Dei Taktlause!",
            plain_text,
            settings.EMAIL_HOST_USER,
            [self.object.email],
            html_message=html,
        )

        return response


class ProfileDetail(LoginRequiredMixin, DetailView):
    """View for user profiles."""

    model = UserCustom
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

class MemberList(ListView):

    model= UserCustom
    template_name = "accounts/member_list.html"
    context_object_name = "medlemmer"
