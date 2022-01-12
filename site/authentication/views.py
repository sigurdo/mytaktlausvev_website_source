from django.contrib.auth.views import LoginView

from .forms import LoginForm


class LoginViewCustom(LoginView):
    template_name = "authentication/login.html"
    authentication_form = LoginForm

    def get_initial(self):
        initial = super().get_initial()
        initial[self.redirect_field_name] = self.get_redirect_url()
        return initial

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Logg inn"
        return super().get_context_data(**kwargs)
